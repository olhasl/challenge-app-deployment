import pandas as pd
import os

def zip_to_province(zip):
    """
    Maps a Belgian postal code to its corresponding province.
    Parameters: 
        zip : int or str
    Returns: 
        str
    """
    first_two_digits = int(str(zip)[:2])
    if 10 <= first_two_digits <= 12:
        property_province = "Brussels-Capital Region"
    elif 13 <= first_two_digits <= 14:
        property_province = "Province of Walloon Brabant"
    elif 15 <= first_two_digits <= 19 or 30 <= first_two_digits <= 34:
        property_province = "Province of Flemish Brabant"
    elif 20 <= first_two_digits <= 29:
        property_province = "Province of Antwerp"
    elif 35 <= first_two_digits <= 39:
        property_province = "Province of Limburg"
    elif 40 <= first_two_digits <= 49:
        property_province = "Province of Liège"
    elif 66 <= first_two_digits <= 69:
        property_province = "Province of Luxembourg"
    elif 50 <= first_two_digits <= 56:
        property_province = "Province of Namur"
    elif 60 <= first_two_digits <= 65 or 70 <= first_two_digits <= 79:
        property_province = "Province of Hainaut"
    elif 80 <= first_two_digits <= 89:
        property_province = "Province of West Flanders"
    elif 90 <= first_two_digits <= 99:
        property_province = "Province of East Flanders"
    return property_province

def preprocess(livable_space, property_type, zip_code, property_province, property_state):
    """
    Prepares and transforms property data for prediction.

    This function takes input property attributes, validates them, merges additional
    income data based on postal codes, groups property subtypes into broader categories,
    and formats the data into a structured DataFrame suitable for model prediction.

    Parameters:
        livable_space : int, float, or list of int/float
        property_type : str or list of str
        zip_code : int, str, or list of int/str
        property_province : str or list of str
        property_state : str or list of str

    Returns:
        pd.DataFrame
    """
    # Validating and converting input data into lists
    if not isinstance(livable_space, list):
        livable_space = [livable_space]
    if not isinstance(property_type, list):
        property_type = [property_type]
    if not isinstance(zip_code, list):
        zip_code = [zip_code]
    if not isinstance(property_province, list):
        property_province = [property_province]
    if not isinstance(property_state, list):
        property_state = [property_state]

    # Creating a new DataFrame
    new_data = pd.DataFrame({
        'Livable Space (m2)': livable_space,
        'Subtype of Property': property_type,
        'Zip Code': zip_code,
        'Province': property_province,
        'State of the Building': property_state
    })

    # Load geo_income data
    code_dir = os.path.dirname(os.path.realpath(__file__))
    geo_income_data_path = os.path.join(code_dir, "../model/code_income_data.csv")
    geo_income_data = pd.read_csv(geo_income_data_path, header=0)

    # Type casting for merging
    new_data['Zip Code'] = new_data['Zip Code'].astype(str)
    geo_income_data['Post code'] = geo_income_data['Post code'].astype(str)

    # Data merging
    transform_data = new_data.merge(
        geo_income_data[["Post code", "Avg_Taxable_Income"]],
        how="left",
        left_on="Zip Code",
        right_on="Post code",
    )

    # Removing an unnecessary column
    transform_data.drop(columns=["Zip Code", "Post code"], inplace=True)

    # Grouping property types
    subtype_group_mapping = {
        'house': 'Houses',
        'villa': 'Luxury Properties',
        'town-house': 'Houses',
        'bungalow': 'Houses',
        'farmhouse': 'Houses',
        'country-cottage': 'Houses',
        'chalet': 'Luxury Properties',
        'apartment': 'Apartments',
        'apartment-block': 'Specialized Properties',
        'duplex': 'Apartments',
        'penthouse': 'Apartments',
        'ground-floor': 'Apartments',
        'flat-studio': 'Apartments',
        'triplex': 'Apartments',
        'service-flat': 'Apartments',
        'mansion': 'Luxury Properties',
        'exceptional-property': 'Luxury Properties',
        'castle': 'Luxury Properties',
        'manor-house': 'Luxury Properties',
        'mixed-use-building': 'Specialized Properties',
        'loft': 'Specialized Properties',
        'kot': 'Apartments',
        'other-property': 'Specialized Properties'
    }

    transform_data['Subtype of Property_Grouped'] = transform_data['Subtype of Property'].replace(subtype_group_mapping)

    # Removing an unnecessary column
    transform_data.drop(columns=["Subtype of Property"], inplace=True)
    transform_data['Livable Space (m2)'] = transform_data['Livable Space (m2)'].astype(int)
    transform_data['Avg_Taxable_Income'] = transform_data['Avg_Taxable_Income'].astype(float)

    # New column order
    new_order = [
        "Livable Space (m2)",
        "Avg_Taxable_Income",
        "Province",
        "State of the Building",
        "Subtype of Property_Grouped"
    ]
    # Reorder columns
    transform_data = transform_data[new_order]

    return transform_data
