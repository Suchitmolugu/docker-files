import streamlit as st
import pandas as pd
import datetime
import random
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Train Ticket Booking System",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .booking-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Mock train data
TRAINS = {
    "12345": {"name": "Rajdhani Express", "from": "Delhi", "to": "Mumbai", 
              "departure": "16:00", "arrival": "08:00", "duration": "16h", 
              "classes": {"Sleeper": 500, "3AC": 1500, "2AC": 2500, "1AC": 4000},
              "seats": {"Sleeper": 100, "3AC": 80, "2AC": 50, "1AC": 30}},
    "67890": {"name": "Shatabdi Express", "from": "Delhi", "to": "Chandigarh", 
              "departure": "07:00", "arrival": "11:00", "duration": "4h",
              "classes": {"Chair Car": 800, "Executive": 1500},
              "seats": {"Chair Car": 120, "Executive": 60}},
    "24680": {"name": "Duronto Express", "from": "Kolkata", "to": "Delhi", 
              "departure": "20:00", "arrival": "10:00", "duration": "14h",
              "classes": {"Sleeper": 600, "3AC": 1800, "2AC": 3000, "1AC": 5000},
              "seats": {"Sleeper": 90, "3AC": 70, "2AC": 40, "1AC": 20}},
    "13579": {"name": "Garib Rath", "from": "Mumbai", "to": "Chennai", 
              "departure": "22:00", "arrival": "14:00", "duration": "16h",
              "classes": {"3AC": 1200, "Sleeper": 400},
              "seats": {"3AC": 100, "Sleeper": 120}},
}

CITIES = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", 
          "Ahmedabad", "Pune", "Jaipur", "Lucknow", "Chandigarh"]

def login_page():
    """Login/Signup page"""
    st.title("🚂 Train Ticket Booking System")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.rerun()
            else:
                st.error("Please enter username and password")
    
    with col2:
        st.subheader("New User? Sign Up")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email")
        
        if st.button("Sign Up", key="signup_btn"):
            if new_username and new_password and email:
                if new_password == confirm_password:
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Passwords don't match")
            else:
                st.error("Please fill all fields")

def search_trains():
    """Search trains between stations"""
    st.header("🔍 Search Trains")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        from_city = st.selectbox("From", CITIES)
    with col2:
        to_city = st.selectbox("To", CITIES)
    with col3:
        travel_date = st.date_input("Travel Date", min_value=datetime.now().date())
    
    if st.button("Search Trains", type="primary"):
        if from_city == to_city:
            st.warning("Source and destination cannot be same!")
            return
        
        st.subheader(f"🚆 Trains from {from_city} to {to_city} on {travel_date}")
        
        found_trains = []
        for train_id, train_info in TRAINS.items():
            if train_info["from"] == from_city and train_info["to"] == to_city:
                found_trains.append({"train_id": train_id, **train_info})
        
        if found_trains:
            for train in found_trains:
                with st.container():
                    st.markdown(f"""
                    <div class="booking-card">
                        <h3>🚆 {train['name']} ({train['train_id']})</h3>
                        <p><strong>Departure:</strong> {train['departure']} | <strong>Arrival:</strong> {train['arrival']}</p>
                        <p><strong>Duration:</strong> {train['duration']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        class_type = st.selectbox("Class", list(train['classes'].keys()), 
                                                key=f"class_{train['train_id']}")
                    with col2:
                        passengers = st.number_input("Passengers", min_value=1, max_value=10, 
                                                    value=1, key=f"pass_{train['train_id']}")
                    with col3:
                        if st.button(f"Book Now", key=f"book_{train['train_id']}"):
                            book_ticket(train, class_type, passengers, travel_date)
        else:
            st.info("No trains found for this route. Please try different cities.")

def book_ticket(train, class_type, passengers, travel_date):
    """Book ticket function"""
    ticket_id = f"TKT{random.randint(10000, 99999)}"
    fare = train['classes'][class_type] * passengers
    
    booking = {
        "ticket_id": ticket_id,
        "train_name": train['name'],
        "train_id": train['train_id'],
        "from": train['from'],
        "to": train['to'],
        "date": travel_date.strftime("%Y-%m-%d"),
        "class": class_type,
        "passengers": passengers,
        "fare": fare,
        "booking_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Confirmed",
        "pnr": f"PNR{random.randint(1000000000, 9999999999)}"
    }
    
    st.session_state.bookings.append(booking)
    st.success(f"✅ Ticket Booked Successfully! Ticket ID: {ticket_id}")
    time.sleep(1)
    st.rerun()

def view_bookings():
    """View user bookings"""
    st.header("📋 My Bookings")
    
    if not st.session_state.bookings:
        st.info("No bookings found. Please book a ticket first.")
        return
    
    for booking in st.session_state.bookings:
        with st.expander(f"🎫 {booking['train_name']} - {booking['date']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Ticket ID:** {booking['ticket_id']}  
                **PNR Number:** {booking['pnr']}  
                **Train:** {booking['train_name']} ({booking['train_id']})  
                **From:** {booking['from']} → **To:** {booking['to']}  
                **Date:** {booking['date']}  
                """)
            with col2:
                st.markdown(f"""
                **Class:** {booking['class']}  
                **Passengers:** {booking['passengers']}  
                **Total Fare:** ₹{booking['fare']}  
                **Status:** {booking['status']}  
                **Booking Time:** {booking['booking_time']}  
                """)
            
            if st.button(f"Cancel Booking", key=f"cancel_{booking['ticket_id']}"):
                st.session_state.bookings.remove(booking)
                st.success(f"Booking {booking['ticket_id']} cancelled successfully!")
                time.sleep(1)
                st.rerun()

def cancel_ticket():
    """Cancel ticket page"""
    st.header("❌ Cancel Ticket")
    
    if not st.session_state.bookings:
        st.info("No bookings to cancel.")
        return
    
    booking_options = {f"{b['train_name']} - {b['date']} (ID: {b['ticket_id']})": b 
                      for b in st.session_state.bookings}
    
    selected = st.selectbox("Select ticket to cancel", list(booking_options.keys()))
    
    if st.button("Cancel Selected Ticket", type="secondary"):
        booking_to_cancel = booking_options[selected]
        st.session_state.bookings.remove(booking_to_cancel)
        st.success(f"Ticket {booking_to_cancel['ticket_id']} has been cancelled!")
        time.sleep(1)
        st.rerun()

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

def main_app():
    """Main application after login"""
    st.sidebar.image("https://img.icons8.com/color/96/000000/train.png", width=80)
    st.sidebar.title(f"Welcome, {st.session_state.current_user}! 🎉")
    
    # Sidebar navigation
    menu = st.sidebar.radio(
        "Navigation",
        ["Search Trains", "My Bookings", "Cancel Ticket", "Profile"]
    )
    
    if st.sidebar.button("Logout", type="primary"):
        logout()
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Customer Support**  
    📞 1800-123-4567  
    📧 support@trainbook.com  
    """)
    
    if menu == "Search Trains":
        search_trains()
    elif menu == "My Bookings":
        view_bookings()
    elif menu == "Cancel Ticket":
        cancel_ticket()
    elif menu == "Profile":
        st.header("👤 My Profile")
        st.markdown(f"""
        <div class="booking-card">
            <p><strong>Username:</strong> {st.session_state.current_user}</p>
            <p><strong>Member Since:</strong> {datetime.now().strftime("%Y-%m-%d")}</p>
            <p><strong>Total Bookings:</strong> {len(st.session_state.bookings)}</p>
            <p><strong>Total Spent:</strong> ₹{sum(b['fare'] for b in st.session_state.bookings)}</p>
        </div>
        """, unsafe_allow_html=True)

# Main execution
if st.session_state.logged_in:
    main_app()
else:
    login_page()

# Footer
st.markdown("---")
st.markdown("© 2024 Train Ticket Booking System | Safe & Secure Booking")
