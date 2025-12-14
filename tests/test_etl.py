import pandas as pd
import pytest
import os
import ast

# Paths to data files
JSON_FILE = 'steam_games.json'
CSV_FILE = 'steam_games.csv'

def test_json_file_exists():
    """Test if the source JSON file exists."""
    assert os.path.exists(JSON_FILE), f"{JSON_FILE} not found."

def test_csv_file_exists():
    """Test if the source CSV file exists."""
    assert os.path.exists(CSV_FILE), f"{CSV_FILE} not found."

def test_json_loading_and_structure():
    """Test if the JSON file can be loaded and has basic structure."""
    if not os.path.exists(JSON_FILE):
        pytest.skip("JSON file not found")
    
    rows = []
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            # Read first 100 lines for testing to avoid loading huge file
            for i, line in enumerate(f):
                if i >= 100:
                    break
                rows.append(ast.literal_eval(line))
        
        df = pd.DataFrame(rows)
        
        # Check for expected columns based on main.py usage
        expected_columns = ['release_date', 'genres', 'title', 'specs', 'early_access', 'sentiment', 'metascore']
        # Note: 'metascore' might not be in all rows or might be in different format, 
        # but verifying if critical columns exist in the dataframe is good.
        # Based on main.py: df['release_date'], df['genres'], df['title'], df['specs'], df['early_access'], df['sentiment']
        
        for col in ['release_date', 'genres', 'title', 'specs', 'early_access', 'sentiment']:
            assert col in df.columns, f"Column {col} missing in JSON data"
            
    except Exception as e:
        pytest.fail(f"Failed to load JSON data: {e}")

def test_csv_loading_and_structure():
    """Test if the CSV file can be loaded and has basic structure."""
    if not os.path.exists(CSV_FILE):
        pytest.skip("CSV file not found")
        
    try:
        # Read only a few rows
        df = pd.read_csv(CSV_FILE, nrows=100)
        
        # Check columns used in model.py
        # model.py uses: release_year, early_access, metascore, price
        expected_columns = ['release_year', 'early_access', 'metascore', 'price']
        
        for col in expected_columns:
            assert col in df.columns, f"Column {col} missing in CSV data"
            
    except Exception as e:
        pytest.fail(f"Failed to load CSV data: {e}")

def test_data_types_csv():
    """Validate data types for critical columns in CSV."""
    if not os.path.exists(CSV_FILE):
        pytest.skip("CSV file not found")
        
    df = pd.read_csv(CSV_FILE, nrows=100)
    
    # Check that price is numeric
    assert pd.api.types.is_numeric_dtype(df['price']), "Price should be numeric"
    
    # Check that release_year is numeric
    assert pd.api.types.is_numeric_dtype(df['release_year']), "release_year should be numeric"
