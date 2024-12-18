# App-deployment

- Repository: `https://github.com/olhasl/challenge-app-deployment`
- Type of Challenge: `Learning`
- Duration: `5 days`
- Deadline: `18/12/2024 17:00`
- Presentation: `20/12/2024 10:30`
- Team challenge : Solo

## Table of Contents
1. [Description](#Description)
2. [Installation](#installation)
3. [Usage](#usage)

## **Description**
This is the fourth phase of a large project for predicting real estate sales prices in Belgium. The current task is to create an app to let play with created model and make predictions on an app. This project demonstrates the deployment of a **machine learning model** for predicting real estate prices. Using **Streamlit**, an interactive app that allows users to input property features and obtain price predictions was created. The app is designed for **"ImmoEliza"**, a real estate company, to evaluate property prices and help users make informed decisions.

## **App Features**
1. **Interactive Interface:**  
   Users can manually input property features (type, size, location, state) to receive a predicted price.
   
2. **Real-Time Predictions:**  
   The app uses a pre-trained **CatBoost regression model** to estimate property prices instantly.

3. **Robust Preprocessing Pipeline:**  
   Data validation and preprocessing ensure accurate predictions, even when some inputs are incomplete.

4. **Easy Deployment:**  
   The app is hosted on **Streamlit Community Cloud**, making it accessible anytime.

---

### 1. ***Preprocessing Pipeline***
Located in the `preprocessing/cleaning_data.py`, the `preprocess()` function:
- Validates user inputs for required fields.
- Fills missing values and transforms data into a format suitable for the ML model.
- Ensures text fields (e.g., property type) are mapped to predefined categories.

### 2. ***Prediction Logic***
Located in the `predict/prediction.py`, the `predict()` function:
- Takes preprocessed data as input.
- Uses the pre-trained **CatBoost** model stored in `model/model.cbm` to predict the price.

### 3. ***Streamlit App***
- The `app.py` file serves as the main entry point.
- Users can input features like property type, livable space, zip code, and building state.
- After submission, the app displays a **predicted price**.

---

## **Installation**
1. Clone the repository: 
```https://github.com/olhasl/challenge-app-deployment```
2. Install dependencies: 
  - ```pip install -r requirements.txt```
3. Run the app locally:
```streamlit run app.py```
4. Access the app in a browser at http://localhost:8502

---

## **Usage**

- *Run the app:* 
    - locally (streamlit run main.py)   
        or  
    - open the displayed URL in your browser (https://real-estate-price.streamlit.app)
- *Input Property Features:*   
Enter the property's subtype, livable space, condition, and postal code.

- *Predict Prices:*   
Click the "Predict Price" button to get a real-time price prediction.

- *Interactive Real Estate Insights:*    
Use the app to evaluate property prices interactively.