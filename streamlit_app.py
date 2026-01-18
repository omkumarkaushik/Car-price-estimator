import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Car Price Estimator",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Price Estimator")
st.write("Estimate the price of your car based on its type and specifications")

# API endpoint
API_URL = "http://localhost:8000"

# Check API health
try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code != 200:
        st.error("❌ Backend API is not responding. Please make sure FastAPI is running.")
except:
    st.error("❌ Cannot connect to backend. Make sure to run: `uvicorn app.main:app --reload`")

st.divider()

# Sidebar for navigation
page = st.sidebar.radio("Navigation", ["Home", "Estimate Price"])

if page == "Home":
    st.subheader("Welcome!")
    st.write("""
    This application helps you estimate car prices based on various parameters.
    
    **Features:**
    - Input car details (name, type, base price)
    - Get estimated price based on car type
    - View historical estimates
    
    Navigate to "Estimate Price" to get started!
    """)
    
    # Test API connection
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.success("✅ Connected to backend API")
            st.info(response.json()["message"])
    except:
        pass

elif page == "Estimate Price":
    st.subheader("Enter Car Details")
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        car_name = st.text_input("Car Name", placeholder="e.g., Toyota Camry")
    
    with col2:
        car_type = st.selectbox(
            "Car Type",
            ["sedan", "suv", "truck", "coupe", "hatchback", "other"]
        )
    
    base_price = st.number_input(
        "Base Price ($)",
        min_value=0.0,
        value=20000.0,
        step=1000.0
    )
    
    description = st.text_area(
        "Car Description",
        placeholder="Enter a brief description of the car...",
        height=100
    )
    
    st.divider()
    
    # Estimate button
    if st.button("📊 Get Price Estimate", type="primary", use_container_width=True):
        if car_name and car_type and base_price > 0:
            try:
                # Prepare request
                car_data = {
                    "name": car_name,
                    "type": car_type,
                    "price": base_price,
                    "description": description if description else "No description provided"
                }
                
                # Make API request
                response = requests.post(
                    f"{API_URL}/carPriceEstimator",
                    json=car_data
                )
                
                if response.status_code == 200:
                    estimated_price = response.json()
                    
                    # Display results
                    st.success("✅ Price Estimate Generated!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Base Price", f"${base_price:,.2f}")
                    
                    with col2:
                        markup = estimated_price - base_price
                        st.metric("Markup", f"${markup:,.2f}")
                    
                    with col3:
                        st.metric("Estimated Price", f"${estimated_price:,.2f}", 
                                 delta=f"+${markup:,.2f}", delta_color="off")
                    
                    # Summary
                    st.info(f"""
                    **Car Summary:**
                    - Name: {car_name}
                    - Type: {car_type.capitalize()}
                    - Description: {description if description else "No description provided"}
                    """)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the API. Is FastAPI running?")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields with valid values")
