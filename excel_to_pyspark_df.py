import pandas as pd

def excel_to_pandas_df(excel_file, sheet_name=0):
    """
    Reads an Excel file into a Pandas DataFrame.

    Parameters:
        excel_file (str): Path to the Excel file.
        sheet_name (str or int): Sheet name or index to read. Default is the first sheet.

    Returns:
        pandas.DataFrame: Pandas DataFrame containing the Excel data.
    """
    try:
        # Read the Excel file into a Pandas DataFrame
        pandas_df = pd.read_excel(excel_file, sheet_name=sheet_name)
        return pandas_df
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    excel_file_path1 = "C:\\Users\\kchhatbar\\OneDrive - Deloitte (O365D)\\Documents\\AMEX\\copilot\\data_mapping\\mapped_output.xlsx"
    excel_file_path2 = "C:\\Users\\kchhatbar\\OneDrive - Deloitte (O365D)\\Documents\\AMEX\\copilot\\data_mapping\\cust_output.xlsx"
    df1 = excel_to_pandas_df(excel_file_path1)
    df2 = excel_to_pandas_df(excel_file_path2)
    print(df1.head())
    print(df2.head())

    # Display column names of both DataFrames
    print("Columns in df1:", df1.columns)
    print("Columns in df2:", df2.columns)    # Mapping dictionary for similar columns
    column_mapping = {
        "Cust_number": "Emp_Id",
        "Cust_NAME": "FULL_NAME"
        # Note: Cust_phone_number doesn't have a direct match in df1
    }

    # Rename columns in df2 to match df1 using the mapping
    df2_renamed = df2.rename(columns=column_mapping)

    # Display the renamed DataFrame
    print("Renamed df2:")
    print(df2_renamed.head())