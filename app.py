# for running : & "d:\My Projects\Krishimitra-app\venv\Scripts\python.exe" app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, inspect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import re
from datetime import datetime, date, timedelta
import pytz
from urllib.parse import quote_plus
import random
from functools import wraps
import time
import cloudinary
import cloudinary.uploader
# Added Flask-Mail import
from flask_mail import Mail, Message as FlaskMessage

# --- Local Module Imports ---
from ml_model.predictor import predict_disease, get_crop_advice
from scripts.price_scraper import get_market_prices

# --- Initial Setup ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'krishimitra-secure-secret-key-2025')

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

# --- Flask-Mail SMTP Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'deeprajabhang@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '') 
mail = Mail(app)

# --- Database Configuration ---
project_dir = os.path.dirname(os.path.abspath(__file__))
default_sqlite_path = os.path.join(project_dir, "instance", "krishimitra.sqlite")
os.makedirs(os.path.join(project_dir, "instance"), exist_ok=True)

def get_working_db_uri():
    db_url = os.getenv('DATABASE_URL')
    sqlite_uri = f"sqlite:///{default_sqlite_path}"
    if not db_url:
        return sqlite_uri
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    if db_url.startswith("postgresql://"):
        try:
            import psycopg2
            from urllib.parse import urlparse
            parsed = urlparse(db_url)
            conn = psycopg2.connect(
                dbname=parsed.path.lstrip('/'),
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port or 5432,
                connect_timeout=3,
                sslmode='require'
            )
            conn.close()
            print("[INFO] Connected to remote PostgreSQL database.")
            return db_url
        except Exception as err:
            print(f"[WARNING] Remote PostgreSQL unreachable ({err}). Using local SQLite database.")
            return sqlite_uri
    return db_url

app.config['SQLALCHEMY_DATABASE_URI'] = get_working_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Upload Folders Configuration ---
app.config['LEAF_UPLOAD_FOLDER'] = os.path.join(project_dir, 'static', 'leaf_uploads')
app.config['PRODUCT_UPLOAD_FOLDER'] = os.path.join(project_dir, 'static', 'product_uploads')
os.makedirs(app.config['LEAF_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PRODUCT_UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref='seller_user', lazy=True)
    services = db.relationship('Service', backref='provider', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_details = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True, cascade="all, delete-orphan")
    product = db.relationship('Product', backref='conversations')
    service = db.relationship('Service', backref='conversations')
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    seller = db.relationship('User', foreign_keys=[seller_id])

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id])

# --- Database Table Initialization ---
with app.app_context():
    try:
        inspector = inspect(db.engine)
        if not inspector.has_table("user"):
            print("[INFO] Database tables not found, creating them...")
            db.create_all()
            print("[INFO] Database tables created.")
        else:
            print("[INFO] Database tables verified.")
    except Exception as e:
        print(f"[WARNING] Database check notice: {e}")
        db.create_all()
        print("[INFO] Database tables initialized.")

# --- Template Filters ---
@app.template_filter('format_markdown')
def format_markdown_filter(text):
    """Simple markdown formatter converting bold, lists, and linebreaks into clean HTML."""
    if not text:
        return ""
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    formatted = re.sub(r'^\s*[\*\-]\s+(.*)$', r'<li>\1</li>', formatted, flags=re.MULTILINE)
    formatted = re.sub(r'((?:<li>.*?</li>\s*)+)', r'<ul class="mb-2">\1</ul>', formatted)
    formatted = formatted.replace('\n\n', '<br><br>').replace('\n', '<br>')
    return formatted

# --- Helper Functions and Decorators ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_product_image(file_storage):
    """Uploads to Cloudinary if configured; otherwise saves locally in static/product_uploads/."""
    if not file_storage or file_storage.filename == '':
        return None
    if os.getenv('CLOUDINARY_CLOUD_NAME') and os.getenv('CLOUDINARY_API_KEY'):
        try:
            upload_result = cloudinary.uploader.upload(file_storage)
            secure_url = upload_result.get('secure_url')
            if secure_url:
                return secure_url
        except Exception as e:
            print(f"[WARNING] Cloudinary upload failed ({e}). Falling back to local storage.")

    upload_folder = app.config['PRODUCT_UPLOAD_FOLDER']
    orig_name = secure_filename(file_storage.filename) or 'product.jpg'
    unique_filename = f"{int(time.time())}_{orig_name}"
    file_path = os.path.join(upload_folder, unique_filename)
    file_storage.seek(0)
    file_storage.save(file_path)
    return unique_filename

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') not in ['seller', 'admin']:
            flash('Only registered sellers can list products for sale.', 'error')
            return redirect(url_for('store'))
        return f(*args, **kwargs)
    return decorated_function
    
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('You do not have the required administrative permissions to access this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def get_market_status():
    IST = pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    if now.weekday() == 6:
        return "Sunday is an APMC mandi holiday, markets are closed.", False
    if 10 <= now.hour < 18:
        return f"APMC Market is currently OPEN. (Current time: {now.strftime('%I:%M %p')} IST)", True
    else:
        return f"APMC Market is currently CLOSED (Regular hours: 10 AM - 6 PM IST). (Current time: {now.strftime('%I:%M %p')})", False

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname', '').strip()
        email = request.form.get('email', '').strip().lower()
        mobile = request.form.get('mobile', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'customer').strip()

        if not fullname or not email or not mobile or not password:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match. Please re-enter your password.', 'error')
            return redirect(url_for('register'))

        if len(mobile) != 10 or not mobile.isdigit():
            flash('Please enter a valid 10-digit mobile number.', 'error')
            return redirect(url_for('register'))

        if User.query.filter(or_(User.email == email, User.mobile == mobile)).first():
            flash('An account with this email address or mobile number already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            name=fullname,
            email=email,
            mobile=mobile,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in to your new account.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = (request.form.get('email') or request.form.get('username') or '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter(or_(User.email == identifier, User.mobile == identifier)).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            session['role'] = user.role
            flash(f'Logged in successfully! Welcome, {user.name}.', 'success')
            return redirect(url_for('store'))
        else:
            flash('Invalid email/mobile or password. Please try again.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            otp = str(random.randint(100000, 999999))
            session['reset_otp'] = otp
            session['reset_user'] = user.email
            session['reset_time'] = time.time()
            
            print(f"\n[PASSWORD RESET OTP for {user.email}]: {otp}\n")
            
            try:
                msg = FlaskMessage(
                    subject="Krishimitra - Password Reset OTP",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user.email]
                )
                msg.body = f"Hello {user.name},\n\nYour OTP for resetting your Krishimitra password is: {otp}.\n\nThis OTP is valid for 10 minutes.\n\nBest regards,\nTeam Krishimitra"
                mail.send(msg)
                flash('An OTP has been sent securely to your registered email address.', 'success')
            except Exception as e:
                print(f"[INFO] SMTP dispatch note: {e}")
                flash(f'An OTP has been generated for {user.email}. (Check email or server console for OTP).', 'info')
            return redirect(url_for('verify_otp'))
        else:
            flash('This email address is not registered with Krishimitra.', 'error')
    return render_template('forgot_password.html')

@app.route('/store')
def store():
    query = Product.query
    search_term, category = request.args.get('search', '').lower(), request.args.get('category')
    if category: query = query.filter(Product.category == category)
    if search_term: query = query.filter(or_(Product.name.ilike(f'%{search_term}%'), Product.description.ilike(f'%{search_term}%')))
    products = query.order_by(Product.id.desc()).all()
    amazon_link, flipkart_link = None, None
    if not products and search_term:
        url_safe_keyword = quote_plus(search_term)
        amazon_link = f"https://www.amazon.in/s?k={url_safe_keyword}"
        flipkart_link = f"https://www.flipkart.com/search?q={url_safe_keyword}"
    return render_template('store.html', products=products, active_category=category, search_query=search_term, amazon_link=amazon_link, flipkart_link=flipkart_link)

@app.route('/add_product', methods=['GET', 'POST'])
@seller_required
def add_product():
    if request.method == 'POST':
        file_to_upload = request.files.get('image')
        image_identifier = save_uploaded_product_image(file_to_upload)
        if not image_identifier:
            flash('Please select an image file for the product.', 'error')
            return redirect(request.url)

        new_product = Product(
            name=request.form.get('name', '').strip(),
            category=request.form.get('category', '').strip(),
            description=request.form.get('description', '').strip(),
            price=request.form.get('price', '').strip(),
            image=image_identifier,
            seller_id=session.get('user_id')
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Your product has been listed successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@seller_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != session.get('user_id') and session.get('role') != 'admin':
        flash('You are not authorized to edit this product listing.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        product.name = request.form.get('name', product.name).strip()
        product.category = request.form.get('category', product.category).strip()
        product.description = request.form.get('description', product.description).strip()
        product.price = request.form.get('price', product.price).strip()

        file_to_upload = request.files.get('image')
        if file_to_upload and file_to_upload.filename != '':
            new_image = save_uploaded_product_image(file_to_upload)
            if new_image:
                product.image = new_image

        db.session.commit()
        flash('Your product has been updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@seller_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != session.get('user_id') and session.get('role') != 'admin':
        flash('You are not authorized to delete this product.', 'error')
        return redirect(url_for('store'))
    
    # Safely delete any conversations referencing this product
    related_convos = Conversation.query.filter_by(product_id=product.id).all()
    for convo in related_convos:
        db.session.delete(convo)

    db.session.delete(product)
    db.session.commit()
    flash(f"Product '{product.name}' has been deleted successfully.", 'success')
    return redirect(url_for('store'))

@app.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.provider_id != session.get('user_id') and session.get('role') != 'admin':
        flash('You are not authorized to edit this service.', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        service.service_type = request.form.get('service_type', service.service_type).strip()
        service.description = request.form.get('description', service.description).strip()
        service.price_details = request.form.get('price_details', service.price_details).strip()
        service.location = request.form.get('location', service.location).strip()
        db.session.commit()
        flash('Your service listing has been updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_service.html', service=service)

@app.route('/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.provider_id != session.get('user_id') and session.get('role') != 'admin':
        flash('You are not authorized to delete this service.', 'error')
        return redirect(url_for('find_services'))

    related_convos = Conversation.query.filter_by(service_id=service.id).all()
    for convo in related_convos:
        db.session.delete(convo)

    db.session.delete(service)
    db.session.commit()
    flash('Service has been deleted successfully.', 'success')
    return redirect(url_for('find_services'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_products = Product.query.filter_by(seller_id=session['user_id']).order_by(Product.id.desc()).all()
    user_services = Service.query.filter_by(provider_id=session['user_id']).order_by(Service.id.desc()).all()
    return render_template('dashboard.html', products=user_products, services=user_services)

@app.route('/detect', methods=['GET', 'POST'])
def disease_detection():
    cache_buster = int(time.time())
    if request.method == 'POST':
        if 'leaf_image' not in request.files or request.files['leaf_image'].filename == '':
            flash('Please choose an image file of the leaf to analyze.', 'error')
            return redirect(request.url)
        file = request.files['leaf_image']
        if file and allowed_file(file.filename):
            leaf_upload_folder = app.config['LEAF_UPLOAD_FOLDER']
            filename = secure_filename(f"{int(time.time())}_{file.filename}")
            leaf_upload_path = os.path.join(leaf_upload_folder, filename)
            file.save(leaf_upload_path)
            prediction_data = predict_disease(leaf_upload_path)
            keyword = prediction_data.get('product_keyword')
            suggested_products, amazon_link, flipkart_link = [], None, None
            if keyword:
                suggested_products = Product.query.filter(or_(Product.name.ilike(f'%{keyword}%'), Product.description.ilike(f'%{keyword}%'))).all()
                url_safe_keyword = quote_plus(keyword)
                amazon_link = f"https://www.amazon.in/s?k={url_safe_keyword}"
                flipkart_link = f"https://www.flipkart.com/search?q={url_safe_keyword}"
            return render_template('disease_detection.html', prediction_data=prediction_data, uploaded_image=filename, products=suggested_products, amazon_link=amazon_link, flipkart_link=flipkart_link, cache_buster=cache_buster)
        else:
            flash('Invalid image file format. Please upload a PNG, JPG, or JPEG image.', 'error')
            return redirect(request.url)
    return render_template('disease_detection.html', prediction_data=None, cache_buster=cache_buster)

@app.route('/prices')
@app.route('/market_prices')
def market_prices():
    markets = ["Pune", "Nashik", "Mumbai", "Nagpur", "Satara", "Kolhapur", "Ahmednagar", "Akola", "Aurangabad", "Baramati", "Dhule", "Jalgaon", "Latur", "Nanded", "Osmanabad", "Rahuri", "Sangamner"]
    commodities = ["Tomato", "Onion", "Potato", "Brinjal", "Cabbage", "Cauliflower", "Lady's Finger", "Bitter Gourd", "Bottle Gourd", "Cucumber", "Green Chilli", "Garlic", "Ginger(Green)", "Lemon"]
    selected_market = request.args.get('market')
    selected_commodity = request.args.get('commodity')
    date_choice = request.args.get('date', 'today')
    if date_choice == 'yesterday':
        target_date = date.today() - timedelta(days=1)
    else:
        target_date = date.today()
    date_str = target_date.strftime('%Y-%m-%d')
    price_data = get_market_prices(market=selected_market, commodity=selected_commodity, date_str=date_str)
    market_status_message, market_is_open = get_market_status()
    return render_template('market_prices.html', prices=price_data, markets=markets, commodities=commodities, selected_market=selected_market, selected_commodity=selected_commodity, date_choice=date_choice, market_status_message=market_status_message, market_is_open=market_is_open)

@app.route('/conversation/start/product/<int:product_id>')
@login_required
def conversation_start_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id == session['user_id']:
        flash('You cannot start a conversation with yourself.', 'error')
        return redirect(url_for('store'))
    convo = Conversation.query.filter_by(product_id=product.id, buyer_id=session['user_id']).first()
    if not convo:
        convo = Conversation(product_id=product.id, buyer_id=session['user_id'], seller_id=product.seller_id)
        db.session.add(convo)
        db.session.commit()
    return redirect(url_for('conversation_chat', convo_id=convo.id))

@app.route('/conversation/start/service/<int:service_id>')
@login_required
def conversation_start_service(service_id):
    service = Service.query.get_or_404(service_id)
    if service.provider_id == session['user_id']:
        flash('You cannot start a conversation with yourself.', 'error')
        return redirect(url_for('find_services'))
    convo = Conversation.query.filter_by(service_id=service.id, buyer_id=session['user_id']).first()
    if not convo:
        convo = Conversation(service_id=service.id, buyer_id=session['user_id'], seller_id=service.provider_id)
        db.session.add(convo)
        db.session.commit()
    return redirect(url_for('conversation_chat', convo_id=convo.id))

@app.route('/conversation/chat/<int:convo_id>', methods=['GET', 'POST'])
@login_required
def conversation_chat(convo_id):
    convo = Conversation.query.get_or_404(convo_id)
    if session['user_id'] not in [convo.buyer_id, convo.seller_id]:
        flash('You do not have permission to view this conversation.', 'error')
        return redirect(url_for('inbox'))
    if request.method == 'POST':
        text = (request.form.get('message_text') or request.form.get('content') or request.form.get('message') or '').strip()
        if text:
            msg = Message(conversation_id=convo.id, sender_id=session['user_id'], text=text, timestamp=datetime.utcnow())
            db.session.add(msg)
            db.session.commit()
        return redirect(url_for('conversation_chat', convo_id=convo.id))
    return render_template('conversation.html', conversation=convo)

@app.route('/inbox')
@login_required
def inbox():
    conversations = Conversation.query.filter(or_(Conversation.buyer_id == session['user_id'], Conversation.seller_id == session['user_id'])).all()
    conversations.sort(key=lambda c: c.messages[-1].timestamp if c.messages else datetime.min, reverse=True)
    return render_template('inbox.html', conversations=conversations)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/admin')
@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    all_users = User.query.order_by(User.id).all()
    all_products = Product.query.order_by(Product.id.desc()).all()
    user_count = User.query.count()
    product_count = Product.query.count()
    conversation_count = Conversation.query.count()
    return render_template('admin_dashboard.html', users=all_users, products=all_products, user_count=user_count, product_count=product_count, conversation_count=conversation_count)
    
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('You cannot delete your own active administrator account.', 'error')
        return redirect(url_for('admin_dashboard'))

    user_to_delete = User.query.get_or_404(user_id)

    # 1. Delete all messages sent by this user
    Message.query.filter_by(sender_id=user_id).delete()

    # 2. Delete conversations where user is buyer or seller
    user_convos = Conversation.query.filter(or_(Conversation.buyer_id == user_id, Conversation.seller_id == user_id)).all()
    for c in user_convos:
        db.session.delete(c)

    # 3. Delete user's products and their conversations
    user_products = Product.query.filter_by(seller_id=user_id).all()
    for p in user_products:
        prod_convos = Conversation.query.filter_by(product_id=p.id).all()
        for pc in prod_convos:
            db.session.delete(pc)
        db.session.delete(p)

    # 4. Delete user's services and their conversations
    user_services = Service.query.filter_by(provider_id=user_id).all()
    for s in user_services:
        serv_convos = Conversation.query.filter_by(service_id=s.id).all()
        for sc in serv_convos:
            db.session.delete(sc)
        db.session.delete(s)

    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f"User '{user_to_delete.name}' ({user_to_delete.email}) and all associated records have been deleted.", 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    product_to_delete = Product.query.get_or_404(product_id)
    # Safely remove conversations linked to this product first
    Conversation.query.filter_by(product_id=product_to_delete.id).delete()
    db.session.delete(product_to_delete)
    db.session.commit()
    flash(f"Product '{product_to_delete.name}' has been deleted by an administrator.", 'success')
    return redirect(request.referrer or url_for('admin_dashboard'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_otp' not in session or 'reset_user' not in session:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        user_otp = request.form.get('otp', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Check OTP expiry (15 minutes)
        reset_time = session.get('reset_time', 0)
        if time.time() - reset_time > 900:
            session.pop('reset_otp', None)
            session.pop('reset_user', None)
            session.pop('reset_time', None)
            flash('The OTP has expired. Please request a new one.', 'error')
            return redirect(url_for('forgot_password'))

        if user_otp != session.get('reset_otp'):
            flash('Invalid OTP. Please check and try again.', 'error')
            return redirect(url_for('verify_otp'))

        if new_password != confirm_password:
            flash('Passwords do not match. Please re-enter.', 'error')
            return redirect(url_for('verify_otp'))

        user_to_update = User.query.filter_by(email=session['reset_user']).first()
        if user_to_update:
            user_to_update.password = generate_password_hash(new_password)
            db.session.commit()
            session.pop('reset_otp', None)
            session.pop('reset_user', None)
            session.pop('reset_time', None)
            flash('Your password has been reset successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('verify_otp.html')

@app.route('/crop_advisory', methods=['GET', 'POST'])
@login_required
def crop_advisory():
    if request.method == 'POST':
        user_question = request.form.get('user_question', '').strip()
        if user_question:
            ai_answer = get_crop_advice(user_question)
            return render_template('crop_advisory.html', user_question=user_question, ai_answer=ai_answer)
    return render_template('crop_advisory.html', user_question=None, ai_answer=None)

@app.route('/contact', methods=['GET', 'POST'])
@app.route('/contact_admin', methods=['GET', 'POST'])
def contact_admin():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        sender_email = request.form.get('email', '').strip()
        subject = request.form.get('subject', 'Krishimitra Feedback').strip()
        message = request.form.get('message', '').strip()

        admin_email = os.getenv('ADMIN_EMAIL', 'deeprajabhang@gmail.com')
        print(f"\n[CONTACT MESSAGE from {name} ({sender_email})]:\nSubject: {subject}\nMessage: {message}\n")

        try:
            msg = FlaskMessage(
                subject=f"Krishimitra Contact: {subject}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[admin_email]
            )
            msg.body = f"Name: {name}\nEmail: {sender_email}\nSubject: {subject}\n\nMessage:\n{message}"
            mail.send(msg)
            flash('Your message has been sent to the admin. Thank you for reaching out!', 'success')
        except Exception as e:
            print(f"[INFO] Contact form mail notification note: {e}")
            flash('Thank you! Your feedback has been received by our team.', 'success')
        return redirect(url_for('contact_admin'))
    return render_template('contact_admin.html')

@app.route('/services')
def find_services():
    search_location = request.args.get('location', '').strip().lower()
    query = Service.query
    if search_location:
        query = query.filter(Service.location.ilike(f'%{search_location}%'))
    services = query.order_by(Service.id.desc()).all()
    return render_template('find_services.html', services=services, search_location=request.args.get('location', ''))

@app.route('/offer_service', methods=['GET', 'POST'])
@login_required
def offer_service():
    if request.method == 'POST':
        new_service = Service(
            service_type=request.form.get('service_type', '').strip(),
            description=request.form.get('description', '').strip(),
            price_details=request.form.get('price_details', '').strip(),
            location=request.form.get('location', '').strip(),
            provider_id=session['user_id']
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Your agricultural service has been listed successfully!', 'success')
        return redirect(url_for('find_services'))
    return render_template('offer_service.html')

if __name__ == '__main__':
    app.run(debug=True)

