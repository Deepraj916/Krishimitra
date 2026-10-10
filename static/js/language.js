/**
 * Krishimitra - High-Fidelity English-to-Marathi Translation Engine
 * Translates every element, text node, button, input placeholder, and dynamic component.
 */

const MARATHI_DICTIONARY = {
    // Brand & Navigation
    "🌱 Krishimitra": "🌱 कृषीमित्र",
    "Krishimitra": "कृषीमित्र",
    "Agro Store": "कृषी भांडार",
    "Services": "कृषी सेवा",
    "Disease Detection": "पीक रोग निदान",
    "Market Prices": "बाजार भाव (मंडी)",
    "AI Advisor": "AI शेती सल्लागार",
    "Login": "लॉगिन",
    "Register": "नोंदणी करा",
    "My Dashboard": "माझे डॅशबोर्ड",
    "Admin Dashboard": "प्रशासक डॅशबोर्ड",
    "Inbox": "संदेश (इनबॉक्स)",
    "Logout": "लॉगआउट",
    "About Us": "आमच्याबद्दल",
    "Contact Us": "संपर्क साधा",
    "Contact Admin": "प्रशासकाशी संपर्क साधा",

    // Home Page (index.html)
    "Welcome to Krishimitra": "कृषीमित्र मध्ये आपले स्वागत आहे",
    "Your trusted partner in modern agriculture. All the tools and knowledge you need, in one place.": "आधुनिक शेतीमध्ये आपला विश्वासू साथीदार. आपल्याला आवश्यक असलेली सर्व साधने आणि माहिती एकाच ठिकाणी.",
    "Explore the Store": "भांडार एक्सप्लोर करा",
    "Our Core Features": "आमची मुख्य वैशिष्ट्ये",
    "Buy and sell agricultural products, tools, and seeds from a trusted community.": "विश्वासू शेतकरी समुदायाकडून कृषी उत्पादने, साधने आणि बियाणे खरेदी आणि विक्री करा.",
    "Visit Store": "भांडाराला भेट द्या",
    "Seva Kendra": "सेवा केंद्र",
    "Find or offer local agricultural services like tractor work, labor, and spraying.": "ट्रॅक्टर काम, शेतमजूर आणि फवारणी यासारख्या स्थानिक कृषी सेवा शोधा किंवा नोंदवा.",
    "Find Services": "सेवा शोधा",
    "Upload a photo of a plant leaf and get an instant AI-powered diagnosis.": "झाडाच्या पानाचा फोटो अपलोड करा आणि त्वरित AI-आधारित अचूक रोग निदान मिळवा.",
    "Detect Disease": "रोग ओळखा",
    "Get live, up-to-date market prices for agricultural commodities in your region.": "आपल्या भागातील कृषी उत्पादनांचे थेट आणि ताजे बाजार भाव मिळवा.",
    "Check Prices": "भाव तपासा",

    // Disease Detection (disease_detection.html)
    "Plant Disease Detection System": "झाडांच्या रोगांचे AI निदान प्रणाली",
    "Plant Disease Detection": "पीक रोग निदान",
    "Upload a clear photo of an affected plant leaf to get a diagnosis.": "निदान मिळवण्यासाठी बाधित पानाचा स्पष्ट फोटो अपलोड करा.",
    "Choose an Image": "पानाचा फोटो निवडा",
    "Uploaded Image": "अपलोड केलेला फोटो",
    "AI Diagnosis": "AI रोग निदान अहवाल",
    "Plant Identified:": "ओळखलेली वनस्पती:",
    "Plant Identified": "ओळखलेली वनस्पती",
    "Condition:": "आरोग्य स्थिती:",
    "Condition": "आरोग्य स्थिती",
    "Healthy": "निरोगी (रोगमुक्त)",
    "Recommended Fertilizer": "शिफारस केलेले खत",
    "Fertilizer:": "खत:",
    "Fertilizer": "खत",
    "Minimum Quantity for 10 Liters:": "१० लिटर पाण्यासाठी किमान प्रमाण:",
    "Suggested Remedy": "सुचवलेली उपाययोजना व उपचार",
    "Purchase remedy online:": "ऑनलाइन औषध खरेदी करा:",
    "Preview of Selected Leaf": "निवडलेल्या पानाचे पूर्वावलोकन",
    "Analyzing leaf image...": "पानाच्या प्रतिमेचे विश्लेषण करत आहे...",
    "Choose File": "फाइल निवडा",
    "No file chosen": "कोणतीही फाइल निवडलेली नाही",

    // Market Prices (market_prices.html)
    "Real-Time APMC Mandi Market Prices": "थेट कृषी उत्पन्न बाजार समिती (APMC) मंडी भाव",
    "Real-Time Market Prices": "थेट बाजार भाव",
    "Select State:": "राज्य निवडा:",
    "Select District:": "जिल्हा निवडा:",
    "Select Market:": "मंडी / बाजार निवडा:",
    "Select Commodity:": "शेतमाल निवडा:",
    "Select State": "राज्य निवडा",
    "Select District": "जिल्हा निवडा",
    "Select Market": "मंडी निवडा",
    "Select Commodity": "शेतमाल निवडा",
    "All States": "सर्व राज्ये",
    "All Districts": "सर्व जिल्हे",
    "All Markets": "सर्व बाजार",
    "All Commodities": "सर्व शेतमाल",
    "Fetch Prices": "बाजार भाव मिळवा",
    "Filter Prices": "भाव फिल्टर करा",
    "Commodity": "शेतमाल",
    "State": "राज्य",
    "District": "जिल्हा",
    "Market": "मंडी / बाजार",
    "Min Price (₹/Qtl)": "किमान भाव (₹/क्विंटल)",
    "Max Price (₹/Qtl)": "कमाल भाव (₹/क्विंटल)",
    "Modal Price (₹/Qtl)": "सरासरी भाव (₹/क्विंटल)",
    "Date": "दिनांक",
    "No market price records found for this selection.": "या निवडीसाठी कोणतेही बाजार भाव आढळले नाहीत.",
    "Last updated:": "शेवटचे अपडेट:",
    "Arrival Date": "आवक दिनांक",

    // Agro Store (store.html, add_product.html, edit_product.html)
    "Krishimitra Store": "कृषीमित्र कृषी भांडार",
    "Search products...": "उत्पादने शोधा...",
    "Filter by Category": "श्रेणीनुसार फिल्टर करा",
    "All Categories": "सर्व श्रेणी",
    "Crops": "पिके",
    "Vegetables": "भाज्या",
    "Fruits": "फळे",
    "Seeds": "बियाणे",
    "Fertilizers": "खते",
    "Tools & Equipment": "अवजारे आणि उपकरणे",
    "Add New Product": "नवीन उत्पादन जोडा",
    "Add Product": "उत्पादन जोडा",
    "Edit Product": "उत्पादन संपादित करा",
    "Product Name": "उत्पादनाचे नाव",
    "Product Category": "उत्पादनाची श्रेणी",
    "Category": "श्रेणी",
    "Description": "तपशील / वर्णन",
    "Price": "किंमत",
    "Price:": "किंमत:",
    "Product Image": "उत्पादनाचा फोटो",
    "Seller:": "विक्रेता:",
    "Seller": "विक्रेता",
    "Contact Seller": "विक्रेत्याशी संपर्क साधा",
    "Edit": "संपादित करा",
    "Delete": "हटवा",
    "Are you sure you want to delete this product?": "आपण खरोखर हे उत्पादन हटवू इच्छिता?",
    "No products found.": "कोणतीही उत्पादने आढळली नाहीत.",
    "Save Changes": "बदल जतन करा",
    "Back to Store": "भांडारावर परत जा",
    "Submit Product": "उत्पादन सबमिट करा",

    // Services (find_services.html, offer_service.html, edit_service.html)
    "Agricultural Services Directory": "कृषी सेवा निर्देशिका",
    "Find Machinery, Labor & Agri Services": "कृषी अवजारे, मजूर आणि शेती सेवा शोधा",
    "Offer a Service": "नवीन सेवा नोंदवा",
    "Offer Service": "सेवा नोंदवा",
    "Edit Service": "सेवा संपादित करा",
    "Search services...": "सेवा शोधा...",
    "Service Type:": "सेवेचा प्रकार:",
    "Service Type": "सेवेचा प्रकार",
    "Location:": "स्थान / ठिकाण:",
    "Location": "स्थान",
    "Rates:": "दर / किंमत:",
    "Price Details": "किंमतीचा तपशील",
    "Price Details:": "किंमतीचा तपशील:",
    "Contact Provider": "सेवा प्रदात्याशी संपर्क साधा",
    "Provider:": "सेवा प्रदाता:",
    "Provider": "सेवा प्रदाता",
    "Tractor Rental": "ट्रॅक्टर भाड्याने",
    "Harvester Rental": "हार्वेस्टर भाड्याने",
    "Drone Spraying": "ड्रोन फवारणी",
    "Soil Testing": "माती परीक्षण",
    "Farm Labor": "शेतमजूर",
    "No services found.": "कोणत्याही सेवा आढळल्या नाहीत.",
    "Submit Service": "सेवा सबमिट करा",

    // AI Advisor (crop_advisory.html)
    "Krishimitra AI Smart Farming Advisor": "कृषीमित्र AI स्मार्ट शेती सल्लागार",
    "Ask any farming question about crops, weather, pest control, or fertilizers.": "पिके, हवामान, कीड नियंत्रण किंवा खतांबद्दल कोणताही शेतीविषयक प्रश्न विचारा.",
    "Your Question / Query:": "आपला शेतीविषयक प्रश्न:",
    "Type your agricultural question here...": "आपला शेतीविषयक प्रश्न येथे लिहा...",
    "Ask Advisor": "सल्लागाराला विचारा",
    "AI Advice:": "AI शेती सल्ला:",
    "AI Agriculture Advisory": "AI शेती सल्लागार",
    "Ask a Question": "प्रश्न विचारा",
    "Generating AI response...": "AI सल्ला तयार होत आहे...",

    // Dashboard & Chat (dashboard.html, inbox.html, conversation.html)
    "User Profile": "वापरकर्ता माहिती",
    "Full Name:": "पूर्ण नाव:",
    "Email:": "ईमेल:",
    "Mobile:": "मोबाईल:",
    "Role:": "भूमिका:",
    "My Listed Products": "माझी उत्पादने",
    "My Listed Services": "माझ्या सेवा",
    "You haven't listed any products yet.": "तुम्ही अद्याप कोणतीही उत्पादने जोडलेली नाहीत.",
    "You haven't listed any services yet.": "तुम्ही अद्याप कोणतीही सेवा जोडलेली नाही.",
    "My Messages": "माझे संदेश",
    "Conversation with": "यांच्याशी संभाषण:",
    "Type your message...": "आपला संदेश येथे लिहा...",
    "Send": "पाठवा",
    "No messages yet. Start the conversation!": "अद्याप कोणतेही संदेश नाहीत. संभाषण सुरू करा!",
    "Direct Chat": "थेट चॅट संभाषण",

    // Auth & Accounts (login.html, register.html, forgot_password.html, verify_otp.html)
    "Login to Krishimitra": "कृषीमित्र मध्ये लॉगिन करा",
    "Email Address": "ईमेल पत्ता",
    "Enter email": "ईमेल प्रविष्ट करा",
    "Password": "पासवर्ड",
    "Enter password": "पासवर्ड प्रविष्ट करा",
    "Confirm Password": "पासवर्डची पुष्टी करा",
    "Full Name": "पूर्ण नाव",
    "Enter your full name": "आपले पूर्ण नाव प्रविष्ट करा",
    "Mobile Number": "मोबाईल नंबर",
    "Enter 10-digit mobile number": "१० अंकी मोबाईल नंबर प्रविष्ट करा",
    "Select Role": "भूमिका निवडा",
    "Farmer": "शेतकरी",
    "Buyer": "खरेदीदार",
    "Service Provider": "सेवा प्रदाता",
    "Admin": "प्रशासक",
    "Forgot Password?": "पासवर्ड विसरलात?",
    "Reset Password": "पासवर्ड रीसेट करा",
    "Don't have an account?": "खाते नाही का?",
    "Already have an account?": "आधीच खाते आहे का?",
    "Register here": "येथे नोंदणी करा",
    "Login here": "येथे लॉगिन करा",
    "Verify OTP": "OTP सत्यापित करा",
    "Enter OTP": "OTP प्रविष्ट करा",
    "Verify & Proceed": "सत्यापित करा आणि पुढे जा",

    // Admin Dashboard (admin_dashboard.html, contact_admin.html)
    "Total Users": "एकूण वापरकर्ते",
    "Total Products": "एकूण उत्पादने",
    "Total Services": "एकूण सेवा",
    "Manage Users": "वापरकर्ते व्यवस्थापित करा",
    "Manage Products": "उत्पादने व्यवस्थापित करा",
    "Manage Services": "सेवा व्यवस्थापित करा",
    "Contact Administrator": "प्रशासकाशी संपर्क साधा",
    "Subject": "विषय",
    "Message": "संदेश",
    "Send Message": "संदेश पाठवा",

    // About Us (about.html)
    "About Krishimitra": "कृषीमित्र बद्दल माहिती",
    "Empowering Farmers Through Technology": "तंत्रज्ञानाच्या माध्यमातून शेतकऱ्यांचे सक्षमीकरण",
    "Our Mission": "आमचे ध्येय",
    "Our Vision": "आमची दृष्टी",

    // Common Buttons, Badges, Labels
    "Submit": "सबमिट करा",
    "Save": "जतन करा",
    "Cancel": "रद्द करा",
    "Close": "बंद करा",
    "Back": "मागे जा",
    "Loading...": "लोड होत आहे...",
    "Search": "शोधा",
    "Filter": "फिल्टर करा",
    "Clear": "साफ करा",
    "Yes": "होय",
    "No": "नाही",
    "Actions": "कृती",
    "Status": "स्थिती",
    "View": "पहा",
    "View Details": "तपशील पहा",
    "Download": "डाउनलोड करा",
    "Upload": "अपलोड करा",
    "Success": "यशस्वी",
    "Error": "त्रुटी",
    "Warning": "सूचना",
    "Notice": "माहिती",
    "© 2025 Krishimitra": "© २०२५ कृषीमित्र",
    "Krishimitra | About Us | Contact Us": "कृषीमित्र | आमच्याबद्दल | संपर्क साधा"
};

// Sort keys by descending length so multi-word phrases match before individual words
const SORTED_KEYS = Object.keys(MARATHI_DICTIONARY).sort((a, b) => b.length - a.length);

/**
 * Translate a single text string using dictionary mapping
 */
function translateString(text) {
    if (!text || typeof text !== 'string') return text;
    let trimmed = text.trim();
    if (!trimmed) return text;

    // Exact match
    if (MARATHI_DICTIONARY[trimmed]) {
        return text.replace(trimmed, MARATHI_DICTIONARY[trimmed]);
    }

    // Case-insensitive exact match
    const lowerTrim = trimmed.toLowerCase();
    for (let key of SORTED_KEYS) {
        if (key.toLowerCase() === lowerTrim) {
            return text.replace(trimmed, MARATHI_DICTIONARY[key]);
        }
    }

    // Phrase replacements inside the sentence
    let modified = text;
    for (let key of SORTED_KEYS) {
        if (key.length > 2 && modified.includes(key)) {
            modified = modified.split(key).join(MARATHI_DICTIONARY[key]);
        }
    }
    return modified;
}

/**
 * Walk all text nodes and attributes in the element and translate them
 */
function translateElementTree(root) {
    if (!root) return;

    // 1. Walk text nodes
    const walker = document.createTreeWalker(
        root,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode: function(node) {
                if (!node || !node.nodeValue) return NodeFilter.FILTER_REJECT;
                const parent = node.parentElement;
                if (!parent) return NodeFilter.FILTER_REJECT;
                const tag = parent.tagName.toUpperCase();
                if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' || tag === 'TEXTAREA' || parent.id === 'langToggleBtn' || parent.closest('#langToggleBtn')) {
                    return NodeFilter.FILTER_REJECT;
                }
                if (node.nodeValue.trim().length === 0) return NodeFilter.FILTER_REJECT;
                return NodeFilter.FILTER_ACCEPT;
            }
        },
        false
    );

    let currentNode;
    while (currentNode = walker.nextNode()) {
        if (currentNode._krishi_orig_en === undefined) {
            currentNode._krishi_orig_en = currentNode.nodeValue;
        }
        const translated = translateString(currentNode._krishi_orig_en);
        if (translated !== currentNode.nodeValue) {
            currentNode.nodeValue = translated;
        }
    }

    // 2. Translate attributes on inputs, buttons, etc.
    const formElements = root.querySelectorAll('input, textarea, button, select, option');
    formElements.forEach(el => {
        if (el.closest('#langToggleBtn')) return;

        // Placeholders
        if (el.placeholder) {
            if (el._krishi_orig_placeholder === undefined) {
                el._krishi_orig_placeholder = el.placeholder;
            }
            el.placeholder = translateString(el._krishi_orig_placeholder);
        }

        // Title tooltips
        if (el.title) {
            if (el._krishi_orig_title === undefined) {
                el._krishi_orig_title = el.title;
            }
            el.title = translateString(el._krishi_orig_title);
        }

        // Submit/Button values
        if ((el.tagName === 'INPUT' && (el.type === 'submit' || el.type === 'button')) || el.tagName === 'BUTTON') {
            if (el.value && typeof el.value === 'string' && el.value.trim().length > 0) {
                if (el._krishi_orig_value === undefined) {
                    el._krishi_orig_value = el.value;
                }
                el.value = translateString(el._krishi_orig_value);
            }
        }
    });

    // 3. Document Title
    if (document._krishi_orig_title === undefined) {
        document._krishi_orig_title = document.title;
    }
    document.title = translateString(document._krishi_orig_title);
}

/**
 * Restore all elements to original English
 */
function restoreElementTree(root) {
    if (!root) return;

    const walker = document.createTreeWalker(
        root,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode: function(node) {
                if (!node || node._krishi_orig_en === undefined) return NodeFilter.FILTER_REJECT;
                const parent = node.parentElement;
                if (parent && (parent.id === 'langToggleBtn' || parent.closest('#langToggleBtn'))) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        },
        false
    );

    let currentNode;
    while (currentNode = walker.nextNode()) {
        if (currentNode._krishi_orig_en !== undefined) {
            currentNode.nodeValue = currentNode._krishi_orig_en;
        }
    }

    const formElements = root.querySelectorAll('input, textarea, button, select, option');
    formElements.forEach(el => {
        if (el.closest('#langToggleBtn')) return;
        if (el._krishi_orig_placeholder !== undefined) {
            el.placeholder = el._krishi_orig_placeholder;
        }
        if (el._krishi_orig_title !== undefined) {
            el.title = el._krishi_orig_title;
        }
        if (el._krishi_orig_value !== undefined) {
            el.value = el._krishi_orig_value;
        }
    });

    if (document._krishi_orig_title !== undefined) {
        document.title = document._krishi_orig_title;
    }
}

/**
 * Trigger Google Translate Web Element if present
 */
function triggerGoogleTranslate(langCode) {
    try {
        // Set cookies for Google Translate
        const host = window.location.hostname;
        const cookieVal = '/en/' + langCode;
        document.cookie = 'googtrans=' + cookieVal + '; path=/;';
        if (host) {
            document.cookie = 'googtrans=' + cookieVal + '; path=/; domain=' + host + ';';
            document.cookie = 'googtrans=' + cookieVal + '; path=/; domain=.' + host + ';';
        }

        // Trigger the select dropdown if rendered
        const select = document.querySelector('.goog-te-combo');
        if (select) {
            select.value = langCode;
            select.dispatchEvent(new Event('change'));
        }
    } catch (e) {
        console.warn('Google Translate trigger note:', e);
    }
}

/**
 * Update Language Button State and UI
 */
function updateButtonUI(lang) {
    const btn = document.getElementById('langToggleBtn');
    const textSpan = document.getElementById('langBtnText');
    const iconSpan = document.getElementById('langBtnIcon');
    if (!btn) return;

    if (lang === 'mr') {
        btn.classList.remove('btn-outline-light');
        btn.classList.add('btn-warning');
        btn.title = "Switch back to English / इंग्रजीमध्ये वाचा";
        if (textSpan) textSpan.innerText = "English";
        if (iconSpan) iconSpan.className = "bi bi-globe me-1";
    } else {
        btn.classList.remove('btn-warning');
        btn.classList.add('btn-outline-light');
        btn.title = "मराठी मध्ये वाचा / Read in Marathi";
        if (textSpan) textSpan.innerText = "मराठी";
        if (iconSpan) iconSpan.className = "bi bi-translate me-1";
    }
}

/**
 * Toggle website language between English and Marathi
 */
function toggleWebsiteLanguage() {
    const currentLang = localStorage.getItem('krishimitra_lang') || 'en';
    const newLang = (currentLang === 'mr') ? 'en' : 'mr';

    if (newLang === 'mr') {
        localStorage.setItem('krishimitra_lang', 'mr');
        translateElementTree(document.body);
        document.documentElement.setAttribute('lang', 'mr');
        triggerGoogleTranslate('mr');
        updateButtonUI('mr');
    } else {
        localStorage.setItem('krishimitra_lang', 'en');
        restoreElementTree(document.body);
        document.documentElement.setAttribute('lang', 'en');
        triggerGoogleTranslate('en');
        updateButtonUI('en');
    }
}

/**
 * Initialize on page load and watch for dynamic content
 */
document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('krishimitra_lang') || 'en';
    updateButtonUI(savedLang);

    if (savedLang === 'mr') {
        // Translate right away
        translateElementTree(document.body);
        document.documentElement.setAttribute('lang', 'mr');
        triggerGoogleTranslate('mr');

        // And re-run after short delays for late-rendered items (e.g. charts, async tables)
        setTimeout(() => translateElementTree(document.body), 300);
        setTimeout(() => translateElementTree(document.body), 1000);
    }

    // Set up MutationObserver to translate any dynamically added content
    const observer = new MutationObserver(function(mutations) {
        if (localStorage.getItem('krishimitra_lang') === 'mr') {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // ELEMENT_NODE
                        translateElementTree(node);
                    } else if (node.nodeType === 3) { // TEXT_NODE
                        if (node._krishi_orig_en === undefined) {
                            node._krishi_orig_en = node.nodeValue;
                        }
                        node.nodeValue = translateString(node._krishi_orig_en);
                    }
                });
            });
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
