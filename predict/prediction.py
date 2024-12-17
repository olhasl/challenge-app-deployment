import pandas as pd
import numpy as np
from catboost import CatBoostRegressor

def predict(transform_data):
    """
    Adds predictions to the given DataFrame and returns it.

    Parameters:
        new_X (pd.DataFrame): Input features DataFrame.
        new_predictions (np.ndarray or list): Predicted values.

    Returns:
        pd.DataFrame: Updated DataFrame with predictions.
    """
    model_load = CatBoostRegressor()
    model_load.load_model('./model/model.cbm', format = 'cbm')

    cat_features = ["Province", "State of the Building", "Subtype of Property_Grouped"]

    for cat_col in cat_features:
        if cat_col in transform_data.columns:
            transform_data[cat_col] = transform_data[cat_col].astype(str)
    
    transform_data["Livable Space (m2)"] = transform_data["Livable Space (m2)"].astype(int)
    transform_data["Avg_Taxable_Income"] = transform_data["Avg_Taxable_Income"].astype(float)
            
    new_predictions = model_load.predict(transform_data)

    new_predictions_original = np.expm1(new_predictions)
    new_predictions_original = np.round(new_predictions_original, 2)
    # Add predictions to the DataFrame
    transform_data['Predicted Price'] = new_predictions_original

    # Return the updated DataFrame
    return new_predictions_original