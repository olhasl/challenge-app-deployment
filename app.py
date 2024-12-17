import streamlit as st
import pandas as pd
import os
from preprocessing.cleaning_data import zip_to_province, preprocess
from predict.prediction import predict

st.set_page_config(page_title="challenge-app-deployment",  
    page_icon="🏡",  
    layout="centered",  
    initial_sidebar_state="expanded"
)

# Load data
code_dir = os.path.dirname(os.path.realpath(__file__))  # Directory of the script
data_path = os.path.join(code_dir, "./model/code_income_data.csv")

@st.cache_data
def load_data(data_path):
    """Load and cache data from CSV."""
    return pd.read_csv(data_path)

df = load_data(data_path)

# Centered title
st.markdown(
    """
    <div style="text-align: center;">
        <h1>Real Estate Price Forecasting</h1>
        <h5>This app predicts real estate prices based on the CatBoost model</h5>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar for user inputs
with st.sidebar:
    st.markdown('### ')
    st.header("Enter your property characteristics")
    st.markdown('### ')
    property_type = st.selectbox(
        "Subtype of Property", 
        [
            'apartment', 'ground-floor', 'duplex', 'triplex', 'penthouse', 'loft',
            'flat-studio', 'kot', 'service-flat', 'house', 'country-cottage',
            'town-house', 'farmhouse', 'bungalow', 'villa', 'castle', 'chalet',
            'mansion', 'manor-house', 'exceptional-property', 'apartment-block',
            'mixed-use-building', 'other-property'
        ]
    )
    st.markdown('### ')
    livable_space = st.number_input(
        "Property's Livable Space (m2)", 
        min_value=10, max_value=1000
    )
    st.markdown('### ')
    property_state = st.radio(
        "State of Property", 
        [
            'As new', 'Just renovated', 'Good', 'To be done up', 
            'To renovate', 'To restore', 'Not specified'
        ]
    )
    st.markdown('### ')
    zip_code = st.selectbox(
        "Property's Postcode", 
        sorted(df['Post code'].unique())
    )

property_province = zip_to_province(zip_code)

# Function to display user inputs as a table
def show_data(livable_space, property_type, zip_code, property_province, property_state):
    """Display the user's input data in a styled table."""
    data = {
        'Attribute': [
            'Subtype of Property',
            'Livable Space (m2)',
            'State of Property',
            'Province',
            "Property's Postcode"
        ],
        'Value': [
            property_type,
            livable_space,
            property_state,
            property_province,
            zip_code
        ]
    }
    
    st.markdown('### ')
    st.markdown("#### Your Data:")

    st.dataframe(
        pd.DataFrame(data), 
        column_config={
            "Attribute": st.column_config.TextColumn(width="medium"),
            "Value": st.column_config.TextColumn(width="medium"),
        },
        hide_index=True
    )

# Display user input data
show_data(livable_space, property_type, zip_code, property_province, property_state)

# Inject custom CSS for styling the button
st.markdown(
    """
    <style>
        div.stButton > button {
            background-color: #5a9bd4; /* Softer Blue */
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color:  #4178a6; /* Slightly Darker Blue on Hover */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Button for prediction
if st.button("Predict Price"):
    processed_data = preprocess(
        livable_space, property_type, zip_code, property_province, property_state
    )
    predicted_price = predict(processed_data)

    # Format price with spaces as thousands separator
    formatted_price = f"{predicted_price[0]:,.2f}".replace(",", " ").replace(".", ",")

    # Centered success message
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <h2>Predicted Price: € {formatted_price}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
