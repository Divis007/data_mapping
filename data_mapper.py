import pandas as pd
from typing import Dict, Any

def perform_data_mapping(input_file: str, mapping_file: str, output_file: str) -> None:
    """
    Perform data mapping based on mapping configuration from Excel files
    
    Args:
        input_file (str): Path to input Excel file
        mapping_file (str): Path to mapping configuration Excel file
        output_file (str): Path to save mapped data
    """
    # Read input data and mapping configuration
    input_data = pd.read_excel(input_file)
    mapping_config = pd.read_excel(mapping_file)
    
    # Create output dataframe
    output_data = pd.DataFrame()
    
    def extract_domain(email):
        return email.split('@')[1] if '@' in email else ''
    
    def age_category(age):
        if age < 30:
            return 'Young'
        elif age < 45:
            return 'Middle'
        else:
            return 'Senior'
    
    # Apply mapping rules
    for _, mapping in mapping_config.iterrows():
        source_field = mapping['source_field']
        target_field = mapping['target_field']
        transform_rule = mapping['transform_rule']
        
        if transform_rule == 'direct':
            output_data[target_field] = input_data[source_field]
        elif transform_rule == 'uppercase':
            output_data[target_field] = input_data[source_field].str.upper()
        elif transform_rule == 'lowercase':
            output_data[target_field] = input_data[source_field].str.lower()
        elif transform_rule == 'first_three_chars':
            output_data[target_field] = input_data[source_field].str[:3]
        elif transform_rule == 'extract_domain':
            output_data[target_field] = input_data[source_field].apply(extract_domain)
        elif transform_rule == 'age_category':
            output_data[target_field] = input_data[source_field].apply(age_category)
        elif transform_rule == 'before_at':
            output_data[target_field] = input_data[source_field].str.split('@').str[0]
        elif transform_rule == 'first_letter':
            output_data[target_field] = input_data[source_field].str[0]
    
    # Save mapped data
    output_data.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Example usage
    perform_data_mapping(
        'sample_input.xlsx',
        'mapping_rules.xlsx',
        'mapped_output.xlsx'
    )
