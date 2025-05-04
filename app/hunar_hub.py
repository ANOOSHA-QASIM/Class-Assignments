import streamlit as st
import pandas as pd
import uuid
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

# Load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_logo = load_lottieurl("https://lottie.host/6a376ced-4d46-4a26-8b65-a9916e8f87ca/RnXIFF6ihm.json")

# Custom CSS for dark theme, grey sidebar, and fixed logo column background
st.markdown("""
    <style>
    /* Force dark theme on all Streamlit elements */
    body, .main, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"], .stSidebar {
        background-color: #2C2C2C !important;
        color: #FFFFFF !important;
    }
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
    }
    /* Inputs and Selectboxes */
    .stTextInput>div>input, .stSelectbox>div>select, .stMultiSelect>div>div, .stNumberInput>div>input {
        background-color: #2C2C2C !important;
        color: #FFFFFF !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 4px !important;
    }
    /* DataFrame and Tables */
    .stDataFrame, .stDataFrame table, [data-testid="stTable"] {
        background-color: #2C2C2C !important;
        color: #FFFFFF !important;
    }
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #4CAF50 !important;
    }
    /* Text and Alerts */
    .stMarkdown, .stMarkdown p, .stAlert, .stAlert div, [data-testid="stMarkdownContainer"] {
        color: #FFFFFF !important;
    }
    /* Sliders */
    .stSlider [data-testid="stWidgetLabel"], .stSlider div {
        color: #FFFFFF !important;
    }
    /* Ensure no Streamlit default theme overrides */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #1E1E1E !important;
    }
    /* Fix Lottie logo column background */
    [data-testid="stColumn"], .stColumn, [data-testid="stHorizontalBlock"], 
    [data-testid="stVerticalBlock"], .css-1y0vfr, div[data-testid="stBlock"] {
        background-color: #1E1E1E !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# Predefined categories and subcategories with prices
CATEGORIES = {
    "Mehndi Design | مہندی ڈیزائن": {
        "Bridal | برائیڈل": 5000,
        "Party | پارٹی": 2000
    },
    "Stitching & Tailoring | سلائی اور درزی": {
        "Custom Dress | کسٹم ڈریس": 3000,
        "Alterations | ترمیمات": 1000
    },
    "Handmade Crafts | ہاتھ سے بنے دستکاری": {
        "Jewelry | زیورات": 1500,
        "Decor | سجاوٹ": 2000
    },
    "Cooking & Baking | کھانا پکانا اور بیکنگ": {
        "Cakes | کیک": 2500,
        "Meals | کھانے": 1500
    },
    "Teaching & Tutoring | تدریس اور ٹیوشن": {
        "Academic | تعلیمی": 1000,
        "Skill-Based | ہنر پر مبنی": 1200
    }
}

# User class to store user details
class User:
    def __init__(self, name: str, role: str, skills: list = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role  # "Seller" or "Buyer"
        self.skills = skills if skills else []

    def to_dict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Role": self.role,
            "Skills": ", ".join(self.skills) if self.skills else "None"
        }

# Service class to represent a skill/service
class Service:
    def __init__(self, seller_id: str, category: str, subcategory: str, name: str, price: float, description: str):
        self.id = str(uuid.uuid4())
        self.seller_id = seller_id
        self.category = category
        self.subcategory = subcategory
        self.name = name
        self.price = price
        self.description = description
        self.rating = None

    def to_dict(self):
        return {
            "ID": self.id,
            "Category": self.category,
            "Subcategory": self.subcategory,
            "Name": self.name,
            "Price": self.price,
            "Description": self.description,
            "Rating": self.rating if self.rating else "Not Rated"
        }

# HunarHub class to manage users, services, and bookings
class HunarHub:
    def __init__(self):
        self.users = []
        self.services = []
        self.bookings = []

    def add_user(self, name: str, role: str, skills: list = None):
        user = User(name, role, skills)
        self.users.append(user)
        return user

    def add_service(self, seller_id: str, category: str, subcategory: str, name: str, price: float, description: str):
        service = Service(seller_id, category, subcategory, name, price, description)
        self.services.append(service)
        return service

    def book_service(self, buyer_id: str, service_id: str, payment_method: str):
        # Debug: Log booking attempt
        booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        booking = {
            "BuyerID": buyer_id,
            "ServiceID": service_id,
            "BookingDate": booking_date,
            "PaymentMethod": payment_method,
            "PaymentStatus": "Completed"
        }
        self.bookings.append(booking)
        # Debug: Confirm booking added
        st.write(f"DEBUG: Booking added - BuyerID: {buyer_id}, ServiceID: {service_id}")
        return True

    def rate_service(self, service_id: str, rating: int):
        for service in self.services:
            if service.id == service_id:
                service.rating = rating
                return True
        return False

    def get_services(self):
        return [service.to_dict() for service in self.services]

    def get_bookings(self):
        return self.bookings

    def get_seller_bookings(self, seller_id: str):
        bookings = []
        # Debug: Log seller ID and available bookings
        st.write(f"DEBUG: Fetching bookings for SellerID: {seller_id}")
        st.write(f"DEBUG: Total bookings in system: {len(self.bookings)}")
        for service in self.services:
            if service.seller_id == seller_id:
                for booking in self.bookings:
                    if booking["ServiceID"] == service.id:
                        buyer = next((u for u in self.users if u.id == booking["BuyerID"]), None)
                        if buyer:
                            bookings.append({
                                "BuyerName": buyer.name,
                                "ServiceName": service.name,
                                "Category": service.category,
                                "Subcategory": service.subcategory,
                                "BookingDate": booking["BookingDate"],
                                "Rating": service.rating if service.rating else "Not Rated",
                                "PaymentMethod": booking.get("PaymentMethod", "N/A"),
                                "PaymentStatus": booking.get("PaymentStatus", "N/A")
                            })
        # Debug: Log found bookings
       
        return bookings

# AIRecommender class for AI-driven service recommendations
class AIRecommender:
    def __init__(self, hub: HunarHub):
        self.hub = hub

    def recommend_services(self, interests: list):
        services = self.hub.get_services()
        recommendations = [
            service for service in services
            if service["Category"] in interests or service["Subcategory"] in interests
        ]
        return recommendations

# Streamlit App
def main():
    # Initialize session state
    if "hub" not in st.session_state:
        st.session_state.hub = HunarHub()
        st.session_state.recommender = AIRecommender(st.session_state.hub)
    if "user" not in st.session_state:
        st.session_state.user = None

    # Sidebar for navigation and user actions
    with st.sidebar:
        st.header("Navigation 🚀 | نیویگیشن")
        page = st.radio("Go to: | جائیں:", ["Home 🏠 | ہوم", "Seller 🛠️ | سیلر", "Buyer 🛍️ | خریدار"])

        st.header("User Actions 📋 | صارف کے اعمال")
        user_role = st.selectbox("I am a: | میں ہوں:", ["Buyer | خریدار", "Seller | بیچنے والا"])
        user_role = user_role.split(" | ")[0]
        user_name = st.text_input("Your Name | آپ کا نام")
        if user_role == "Seller":
            skills = st.multiselect("Your Skills | آپ کے ہنر", list(CATEGORIES.keys()))
            skills = [s.split(" | ")[0] for s in skills]
        else:
            skills = None
        if st.button("Register 📝 | رجسٹر"):
            if user_name:
                user = st.session_state.hub.add_user(user_name, user_role, skills)
                st.session_state.user = user
                st.success(f"Registered as {user_name} ({user_role})! ✅ | {user_name} ({user_role}) کے طور پر رجسٹرڈ!")
        
            else:
                st.error("Please enter a name 😕 | براہ کرم نام درج کریں۔")

    # Page rendering
    if page == "Home 🏠 | ہوم":
        # Title with Lottie animation
        col1, col2 = st.columns([1, 3])
        with col1:
            if lottie_logo:
                st_lottie(lottie_logo, height=100, key="logo")
            else:
                st.write("Logo failed to load 😕")
        with col2:
            st.title("Hunar Hub 🛠️")
            st.write("Discover & Book Local Skills and Crafts! 🌟 | مقامی ہنر دریافت کریں اور بک کریں!")
        
        st.header("Welcome to Hunar Hub! 🎉 | ہنر ہب میں خوش آمدید!")
        st.markdown("""
        Hunar Hub is your one-stop platform to connect with local artisans and professionals. 
        Whether you're a **seller** offering unique skills or a **buyer** looking for quality services, 
        we've got you covered! Explore services, book with ease, and share your talents with the world. 🌍
        
        **Features**:
        - Sellers: List your services with categories and subcategories, track bookings/ratings 📊
        - Buyers: Browse, book with payment, and rate services 🛍️
        - AI Recommendations: Find services tailored to your interests 🤖
        - Dark Theme: Sleek and modern UI with a grey sidebar 🌑
        - Bilingual: English and Urdu support 🇵🇰
        
        Navigate using the sidebar to get started! 🚀
        """)

    elif page == "Seller 🛠️ | سیلر":
        if st.session_state.user and st.session_state.user.role == "Seller":
            # Debug: Show current user ID
            st.write(f"DEBUG: Current SellerID: {st.session_state.user.id}")
            
            # Seller Dashboard
            st.header("Seller Dashboard 📊 | سیلر ڈیش بورڈ")
            bookings = st.session_state.hub.get_seller_bookings(st.session_state.user.id)
            if bookings:
                df = pd.DataFrame(bookings)
                st.dataframe(df[["BuyerName", "Category", "Subcategory", "ServiceName", "BookingDate", "Rating", "PaymentMethod", "PaymentStatus"]])

            
            # Debug: Show raw bookings data
            st.subheader("Debug: Raw Bookings Data")
            raw_bookings = st.session_state.hub.get_bookings()
            if raw_bookings:
                st.dataframe(pd.DataFrame(raw_bookings))
            else:
                st.write("No bookings in system 😕")

            # Add Service
            st.header("Add a New Service 🎨 | نیا ہنر شامل کریں")
            category = st.selectbox("Category | زمرہ", list(CATEGORIES.keys()))
            category_key = category
            category = category.split(" | ")[0]
            subcategories = list(CATEGORIES[category_key].keys())
            subcategory = st.selectbox("Subcategory | ذیلی زمرہ", subcategories)
            subcategory_key = subcategory
            subcategory = subcategory.split(" | ")[0]
            price = CATEGORIES[category_key][subcategory_key]
            st.write(f"Price | قیمت: {price} PKR")
            service_name = st.text_input("Service Name | ہنر کا نام")
            description = st.text_area("Description | تفصیل")
            if st.button("List Service ➕ | ہنر شامل کریں"):
                if service_name and description:
                    service = st.session_state.hub.add_service(st.session_state.user.id, category, subcategory, service_name, price, description)
                    st.success("Service listed! 🎉 | ہنر شامل کر دیا گیا!")
                    # Debug: Confirm service added
                    st.write(f"DEBUG: ServiceID: {service.id}")
                else:
                    st.error("Please fill all fields 😕 | براہ کرم تمام فیلڈز بھریں۔")
        else:
            st.error("Please register as a Seller to access this page 😕 | براہ کرم سیلر کے طور پر رجسٹر کریں۔")

    elif page == "Buyer 🛍️ | خریدار":
        if st.session_state.user and st.session_state.user.role == "Buyer":
            # Debug: Show current user ID
            st.write(f"DEBUG: Current BuyerID: {st.session_state.user.id}")
            
            # Browse & Book
            st.header("Available Services 🎨 | دستیاب ہنر")
            interests = st.multiselect("Filter by Interest | دلچسپی کے لحاظ سے فلٹر کریں", list(CATEGORIES.keys()))
            interests = [i.split(" | ")[0] for i in interests]
            if interests:
                recommended_services = st.session_state.recommender.recommend_services(interests)
                if recommended_services:
                    df = pd.DataFrame(recommended_services)
                    st.dataframe(df[["Category", "Subcategory", "Name", "Price", "Description", "Rating"]])
                    service_id = st.selectbox("Select Service to Book | بک کرنے کے لئے ہنر منتخب کریں", [s["ID"] for s in recommended_services])
                    st.subheader("Payment Details 💳 | ادائیگی کی تفصیلات")
                    payment_method = st.selectbox("Payment Method | ادائیگی کا طریقہ", ["Credit/Debit Card | کریڈٹ/ڈیبٹ کارڈ", "UPI | یو پی آئی"])
                    if payment_method == "Credit/Debit Card | کریڈٹ/ڈیبٹ کارڈ":
                        card_number = st.text_input("Card Number | کارڈ نمبر", max_chars=16)
                        expiry = st.text_input("Expiry (MM/YY) | ایکسپائری (ماہ/سال)", max_chars=5)
                        cvv = st.text_input("CVV | سی وی وی", max_chars=3)
                        payment_details = f"Card: {card_number[-4:]} (Exp: {expiry})" if card_number else ""
                    else:
                        upi_id = st.text_input("UPI ID | یو پی آئی آئی ڈی")
                        payment_details = f"UPI: {upi_id}"
                    if st.button("Book Service 📅 | ہنر بک کریں"):
                        if payment_method == "Credit/Debit Card | کریڈٹ/ڈیبٹ کارڈ" and (not card_number or not expiry or not cvv):
                            st.error("Please fill all payment fields 😕 | براہ کرم تمام ادائیگی فیلڈز بھریں۔")
                        elif payment_method == "UPI | یو پی آئی" and not upi_id:
                            st.error("Please enter UPI ID 😕 | براہ کرم یو پی آئی آئی ڈی درج کریں۔")
                        else:
                            success = st.session_state.hub.book_service(st.session_state.user.id, service_id, payment_details)
                            if success:
                                st.success("Service booked and payment processed! ✅ | ہنر بک ہو گیا اور ادائیگی مکمل ہو گئی!")
                            else:
                                st.error("Booking failed 😕 | بکنگ ناکام ہو گئی۔")
                else:
                    st.write("No services found for selected interests 😕 | منتخب دلچسپیوں کے لئے کوئی ہنر نہیں ملا۔")
            else:
                services = st.session_state.hub.get_services()
                if services:
                    df = pd.DataFrame(services)
                    st.dataframe(df[["Category", "Subcategory", "Name", "Price", "Description", "Rating"]])
                else:
                    st.write("No services available yet 😕 | ابھی کوئی ہنر دستیاب نہیں ہے۔")

            # Rate a Service
            st.header("Rate a Service ⭐ | ہنر کی درجہ بندی کریں")
            booked_services = [s for s in st.session_state.hub.get_services() if any(b["ServiceID"] == s["ID"] and b["BuyerID"] == st.session_state.user.id for b in st.session_state.hub.get_bookings())]
            if booked_services:
                service_id = st.selectbox("Select Booked Service | بک کیا گیا ہنر منتخب کریں", [s["ID"] for s in booked_services])
                rating = st.slider("Rating (1-5) | درجہ بندی (1-5)", 1, 5)
                if st.button("Submit Rating 🌟 | درجہ بندی جمع کریں"):
                    if st.session_state.hub.rate_service(service_id, rating):
                        st.success("Rating submitted! ✅ | درجہ بندی جمع ہو گئی!")
                    else:
                        st.error("Failed to submit rating 😕 | درجہ بندی جمع کرنے میں ناکامی۔")
        else:
            st.error("Please register as a Buyer to access this page 😕 | براہ کرم خریدار کے طور پر رجسٹر کریں۔")

if __name__ == "__main__":
    main()