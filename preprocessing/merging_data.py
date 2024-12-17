import pandas as pd
import os

def prepare_postal_income_data(geo_data_path, income_data_path, year=2022):
    """
    Prepares a merged DataFrame with postal code and average taxable income.
    
    Parameters:
        geo_data_path (str): Path to the geographical postal codes CSV file.
        income_data_path (str): Path to the income data CSV file.
        year (int): Year to filter the income data. Default is 2022.
    
    Returns:
        pd.DataFrame: Merged DataFrame with postal codes and taxable income.
    """
    # Load geographical data
    df1 = pd.read_csv(geo_data_path, header=0)
    columns_to_keep = ["Post code", "Municipality code"]
    df1 = df1[columns_to_keep]
    df1["Post code"] = df1["Post code"].astype(str)
    df1["Municipality code"] = df1["Municipality code"].astype(int).astype(str)
    df1.drop_duplicates(subset=["Post code"], inplace=True)
    df1 = df1.rename(columns={"Municipality code": "nisCode"})
    
    # Load income data
    df2 = pd.read_csv(income_data_path, header=0)
    df2 = df2.loc[df2["CD_YEAR"] == year]
    df2["CD_MUNTY_REFNIS"] = df2["CD_MUNTY_REFNIS"].astype(str)
    df2["MS_TOT_NET_TAXABLE_INC"] = df2["MS_TOT_NET_TAXABLE_INC"].astype(float)
    df2["MS_NBR_NON_ZERO_INC"] = df2["MS_NBR_NON_ZERO_INC"].astype(int)
    df2["Avg_Taxable_Income"] = round(
        df2["MS_TOT_NET_TAXABLE_INC"] / df2["MS_NBR_NON_ZERO_INC"], 2
    )
    
    # Merge the data
    merged_df = df1.merge(
        df2[["CD_MUNTY_REFNIS", "Avg_Taxable_Income"]],
        how="left",
        left_on="nisCode",
        right_on="CD_MUNTY_REFNIS",
    )
    merged_df.drop(columns=["CD_MUNTY_REFNIS"], inplace=True)
    
    return merged_df

code_dir = os.path.dirname(os.path.realpath(__file__))
geo_data_path = os.path.join(code_dir, "../model/georef-belgium-postal-codes.csv")
income_data_path = os.path.join(code_dir, "../model/TF_PSNL_INC_TAX_MUNTY.csv")

merged_data = prepare_postal_income_data(geo_data_path, income_data_path)
merged_data = merged_data[~merged_data['Post code'].isin(['9', '612'])]

# Save the new DataFrame to CSV file
merged_data_path = os.path.join(code_dir, "../model/code_income_data.csv")
merged_data.to_csv(merged_data_path, index=False)
