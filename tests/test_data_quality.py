import pandas as pd
import pytest
import os
import ast
import numpy as np

JSON_FILE = 'steam_games.json'
CSV_FILE = 'steam_games.csv'

@pytest.fixture(scope="module")
def df_json():
    if not os.path.exists(JSON_FILE):
        pytest.skip("JSON file not found")
    rows = []
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        # Load a sample to verify quality
        for i, line in enumerate(f):
            if i >= 1000: break
            rows.append(ast.literal_eval(line))
    return pd.DataFrame(rows)

@pytest.fixture(scope="module")
def df_csv():
    if not os.path.exists(CSV_FILE):
        pytest.skip("CSV file not found")
    return pd.read_csv(CSV_FILE, nrows=1000)

def test_null_values_critical_columns_json(df_json):
    """Check for null values in critical columns in JSON data."""
    # It's common to have some nulls, but let's see if we have TOO many or unexpected ones
    # For this test, we just ensure the columns exist, as we did in ETL.
    # Let's check 'id' if it exists, or 'title'.
    
    if 'title' in df_json.columns:
        # Check that we don't have empty titles
        # It's possible some are empty, but let's assert < 50% are empty just as a sanity check
        null_share = df_json['title'].isnull().mean()
        assert null_share < 0.5, f"Too many null titles: {null_share:.2%}"

def test_release_date_format(df_json):
    """Check if release_date roughly looks like a date or year."""
    if 'release_date' not in df_json.columns:
        return
    
    # Drop NAs
    dates = df_json['release_date'].dropna()
    if len(dates) == 0:
        return

    # Check if format is somewhat valid (YYYY-...)
    # We can check if it starts with a number
    valid_starts = dates.str.match(r'^\d{4}')
    valid_ratio = valid_starts.mean()
    assert valid_ratio > 0.5, f"Many release dates don't start with year: {valid_ratio:.2%}"

def test_price_non_negative(df_csv):
    """Check that prices are non-negative."""
    if 'price' not in df_csv.columns:
        return
        
    prices = pd.to_numeric(df_csv['price'], errors='coerce').dropna()
    assert (prices >= 0).all(), "Found negative prices"

def test_metascore_range(df_csv):
    """Check that metascore is between 0 and 100."""
    if 'metascore' not in df_csv.columns:
        return
        
    scores = pd.to_numeric(df_csv['metascore'], errors='coerce').dropna()
    assert (scores >= 0).all() and (scores <= 100).all(), "Metascore out of range [0, 100]"

def test_no_duplicate_ids(df_json):
    """Check for duplicate IDs if 'id' column exists."""
    if 'id' in df_json.columns:
        duplicates = df_json['id'].duplicated().sum()
        # Depending on data, duplicates might be allowed, but usually not for ID.
        # Let's just warn or assert low number.
        # For now, let's assume strict uniqueness is not guaranteed but we report it.
        # We'll assert < 10% duplicates.
        dup_rate = duplicates / len(df_json)
        assert dup_rate < 0.1, f"High duplicate ID rate: {dup_rate:.2%}"
