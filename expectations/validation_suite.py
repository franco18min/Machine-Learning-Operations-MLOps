import great_expectations as gx
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logging import logger

def run_validation():
    logger.info("Starting Great Expectations validation suite...")
    
    # 1. Setup Context
    context = gx.get_context()
    
    # 2. Connect to Data
    # We'll use the CSV file for strict validation
    csv_path = "steam_games.csv"
    if not os.path.exists(csv_path):
        logger.error(f"Data file not found: {csv_path}. Make sure DVC pulled the data.")
        return

    datasource_name = "steam_games_datasource"
    asset_name = "steam_games_csv"
    
    try:
        # Try new API (GX 1.0+)
        if hasattr(context, "data_sources"):
             datasource = context.data_sources.add_pandas(datasource_name)
        else:
             # Fallback for older versions
             datasource = context.sources.add_pandas(datasource_name)
             
        asset = datasource.add_csv_asset(name=asset_name, filepath_or_buffer=csv_path)
    except Exception as e:
        logger.warning(f"Could not add asset (might exist): {e}")
        # Retrieve existing
        if hasattr(context, "data_sources"):
            datasource = context.data_sources.get(datasource_name)
        else:
            datasource = context.sources.get(datasource_name)
            
        if datasource:
             asset = datasource.get_asset(asset_name)
        else:
             raise e

    # 3. Define Expectations Suite
    suite_name = "steam_games_quality_suite"
    
    # GX 1.0: Suites management
    try:
        # Try to delete if exists to avoid conflict on save
        context.suites.delete(suite_name)
    except Exception:
        pass
    
    # Create new
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

    # Get a validator
    # GX 1.0: We might need to get a BatchDefinition first
    try:
        batch_definition = asset.add_batch_definition_whole_dataframe("whole_dataframe")
    except Exception:
        # Might already exist
        batch_definition = asset.get_batch_definition("whole_dataframe")
    
    batch_request = batch_definition.build_batch_request()
    
    # Use validator to add expectations to the suite
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )

    # --- Expectations ---
    
    # Schema Checks
    expected_columns = ['release_year', 'early_access', 'metascore', 'price']
    # Note: The CSV might have more columns, but these are critical for ML
    validator.expect_table_columns_to_match_set(
        column_set=expected_columns,
        exact_match=False # Allow extra columns
    )
    
    # Critical Columns should not be null (based on our ETL cleaning logic, raw CSV might have nulls, 
    # but let's assume we want to monitor the RAW quality)
    # Actually, raw CSV *does* have nulls. We should set a threshold (mostly_pct)
    validator.expect_column_values_to_not_be_null(column="release_year", mostly=0.80) 
    validator.expect_column_values_to_not_be_null(column="price", mostly=0.90)

    # Value Ranges
    # Release Year: reasonable range 1970 - 2030
    validator.expect_column_values_to_be_between(
        column="release_year",
        min_value=1970,
        max_value=2030,
        mostly=0.99 # Allow some outliers
    )

    # Price: >= 0
    validator.expect_column_values_to_be_between(
        column="price",
        min_value=0,
        max_value=1000, # Assuming no game costs > $1000
        mostly=0.99
    )

    # Metascore: 0-100
    validator.expect_column_values_to_be_between(
        column="metascore",
        min_value=0,
        max_value=100,
        mostly=0.95 # Some might be missing or invalid
    )
    
    # Uniqueness (if applicable) - 'id' if it exists, but we don't have 'id' in the minimal columns list above.
    # If the CSV has an 'id' or 'url' column we could check uniqueness.
    # Let's check 'title' uniqueness if present, but titles can duplicate. 
    # We'll skip uniqueness for now on these columns.

    # 4. Save Suite
    # validator.save_expectation_suite(discard_failed_expectations=False)
    # In GX 1.0, expectations added via validator might be in-memory on the suite object.
    # We ensure the context has the updated suite.
    # context.suites.add_or_update(validator.expectation_suite) # Not available
    # Since we added the suite to context earlier, and validator uses it, it should be fine.
    
    # 5. Run Checkpoint (Validation)
    checkpoint_name = "steam_games_checkpoint"
    validation_def_name = "steam_games_validation_def"
    
    # Define ValidationDefinition (GX 1.0 pattern)
    # This links the BatchDefinition (data) with the ExpectationSuite (rules)
    try:
         validation_definition = context.validation_definitions.get(validation_def_name)
    except:
         validation_definition = context.validation_definitions.add(
             gx.ValidationDefinition(
                 name=validation_def_name,
                 data=batch_definition,
                 suite=suite
             )
         )

    checkpoint_config = {
        "name": checkpoint_name,
        "validation_definitions": [validation_definition],
        "actions": [
            gx.checkpoint.actions.UpdateDataDocsAction(name="update_all_data_docs")
        ]
    }

    try:
        # Try to delete if exists
        try:
             context.checkpoints.delete(checkpoint_name)
        except:
             pass
        checkpoint = context.checkpoints.add(gx.Checkpoint(**checkpoint_config))
    except Exception as e:
         logger.error(f"Failed to create checkpoint: {e}")
         raise e
    
    results = checkpoint.run()
    
    # 6. Generate Data Docs
    # Context automatically builds docs to the configured store (usually gx/uncommitted/data_docs)
    # We can try to build them explicitly to our report folder if needed, 
    # but standard behavior is creating a static site.
    
    context.build_data_docs()
    
    logger.info("Validation complete.")
    logger.info(f"Success: {results.success}")
    
    # Output report location
    logger.info("Data Docs generated. Open 'gx/uncommitted/data_docs/local_site/index.html' to view.")

if __name__ == "__main__":
    run_validation()
