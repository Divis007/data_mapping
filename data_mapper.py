import pandas as pd
from typing import Dict, Any, List
import os
from collections import defaultdict

def validate_excel_file(file_path: str) -> bool:
    """Validate if the file is a valid Excel file"""
    return file_path.endswith(('.xlsx', '.xls', '.xlsm'))

def perform_data_mapping(input_file: str, mapping_file: str, output_file: str) -> None:
    """
    Perform data mapping based on mapping configuration from Excel files
    
    Args:
        input_file (str): Path to input Excel file
        mapping_file (str): Path to mapping configuration Excel file
        output_file (str): Path to save mapped data
    """
    try:
        # Validate file extensions
        for file_path in [input_file, mapping_file]:
            if not validate_excel_file(file_path):
                raise ValueError(f"Invalid Excel file format: {file_path}")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        # Try to read Excel files with error handling
        try:
            input_data = pd.read_excel(input_file, engine='openpyxl', sheet_name=0)
        except Exception as e:
            print(f"Error reading input file: {input_file}")
            raise

        try:
            mapping_config = pd.read_excel(mapping_file, engine='openpyxl', sheet_name=0)
        except Exception as e:
            print(f"Error reading mapping file: {mapping_file}")
            raise
        
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
        
        # Save with error handling
        try:
            output_data.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Data mapping completed successfully. Output saved to: {output_file}")
        except Exception as e:
            print(f"Error saving output file: {output_file}")
            raise

    except Exception as e:
        print(f"Error occurred during data mapping: {str(e)}")
        raise

def analyze_data_structure(file_path: str) -> Dict:
    """
    Analyze data structure of an Excel file and suggest mappings
    
    Args:
        file_path (str): Path to Excel file to analyze
    Returns:
        Dict: Analysis results including data types and patterns
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        analysis = {
            'columns': {},
            'suggested_mappings': {}
        }
        
        for column in df.columns:
            column_analysis = {
                'data_type': str(df[column].dtype),
                'unique_values': df[column].nunique(),
                'sample_values': df[column].head().tolist(),
                'patterns': detect_patterns(df[column])
            }
            analysis['columns'][column] = column_analysis
            analysis['suggested_mappings'][column] = suggest_transformation(column_analysis)
        
        return analysis
    except Exception as e:
        print(f"Error analyzing data structure: {str(e)}")
        raise

def detect_patterns(series: pd.Series) -> Dict:
    """Detect common patterns in data"""
    patterns = {
        'has_email': series.str.contains('@').any() if series.dtype == 'object' else False,
        'all_uppercase': series.str.isupper().all() if series.dtype == 'object' else False,
        'all_lowercase': series.str.islower().all() if series.dtype == 'object' else False,
        'numeric_only': series.str.isnumeric().all() if series.dtype == 'object' else False
    }
    return patterns

def suggest_transformation(column_analysis: Dict) -> str:
    """Suggest appropriate transformation based on data patterns"""
    patterns = column_analysis['patterns']
    if patterns.get('has_email'):
        return 'extract_domain or before_at'
    elif column_analysis['data_type'] == 'int64':
        return 'age_category if age-related, otherwise direct'
    elif patterns.get('all_uppercase'):
        return 'direct or lowercase'
    elif patterns.get('all_lowercase'):
        return 'direct or uppercase'
    return 'direct'

def reverse_engineer_mapping(input_file: str, target_file: str) -> pd.DataFrame:
    """
    Reverse engineer mapping rules by comparing input and target data structures
    """
    input_analysis = analyze_data_structure(input_file)
    target_analysis = analyze_data_structure(target_file)
    
    suggested_mappings = []
    for target_col, target_info in target_analysis['columns'].items():
        for source_col, source_info in input_analysis['columns'].items():
            if similar_patterns(source_info, target_info):
                suggested_mappings.append({
                    'source_field': source_col,
                    'target_field': target_col,
                    'transform_rule': suggest_transformation(source_info)
                })
    
    return pd.DataFrame(suggested_mappings)

def similar_patterns(source_info: Dict, target_info: Dict) -> bool:
    """Check if two columns have similar patterns"""
    return (
        source_info['data_type'] == target_info['data_type'] or
        (source_info['patterns'].get('has_email') and target_info['patterns'].get('has_email')) or
        (source_info['patterns'].get('numeric_only') and target_info['patterns'].get('numeric_only'))
    )

if __name__ == "__main__":    
    # Use relative paths to avoid path issues
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'sample_input.xlsx')
    mapping_file = os.path.join(base_dir, 'mapping_rules.xlsx')
    output_file = os.path.join(base_dir, 'mapped_output.xlsx')
    
    perform_data_mapping(input_file, mapping_file, output_file)
    
    # Example of reverse engineering
    print("\nReverse Engineering Analysis:")
    analysis = analyze_data_structure(input_file)
    print("\nData Structure Analysis:")
    for column, info in analysis['columns'].items():
        print(f"\nColumn: {column}")
        print(f"Data Type: {info['data_type']}")
        print(f"Sample Values: {info['sample_values']}")
        print(f"Suggested Transformation: {info['suggested_mappings'][column]}")



