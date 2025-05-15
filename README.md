# Data Mapping Reverse Engineering Guide

## What is Reverse Engineering in Data Mapping?
Reverse engineering in data mapping is the process of analyzing existing data structures to:
1. Understand the current data format
2. Detect patterns and relationships
3. Infer transformation rules
4. Generate mapping suggestions

## Key Concepts

### 1. Data Structure Analysis
- Examining data types of each column
- Identifying patterns in data values
- Analyzing value distributions
- Detecting special formats (emails, dates, etc.)

### 2. Pattern Detection
Common patterns include:
- Email addresses
- Uppercase/lowercase text
- Numeric values
- Date formats
- Special characters

### 3. Transformation Rules
Based on patterns, we can suggest:
- Direct mapping
- Case transformations
- Data extraction (e.g., from emails)
- Category mapping (e.g., age groups)

## How to Use

1. Analyze source data:
```python
analysis = analyze_data_structure('sample_input.xlsx')
```

2. View suggestions:
```python
for column, info in analysis['columns'].items():
    print(f"Column {column}: {info['suggested_mappings']}")
```

3. Generate mapping rules:
```python
mappings = reverse_engineer_mapping('source.xlsx', 'target.xlsx')
```
