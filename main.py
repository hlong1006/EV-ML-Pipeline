import sys
from extract import extract_all_data
from transform import transform_data
from load import load_transformed_data

def run_etl_pipeline():
    try:
        df_ev2023, df_ev2024, df_ele = extract_all_data()
        
        if df_ev2023 is None or df_ev2024 is None:
            print("ERROR: Can't extracting data")
            return False
        print(f"  - EV Database 2023: {len(df_ev2023)} dòng")
        print(f"  - EV Database 2024: {len(df_ev2024)} dòng")
        if df_ele is not None:
            print(f"  - EV Spec 2025: {len(df_ele)} dòng")
        
        result = transform_data()
        
        if result is None:
            print("ERROR: Can't transform data")
            return False
        
        df_transformed, label_encoders = result
        success = load_transformed_data(df_transformed, label_encoders)
        
        if not success:
            print("ERROR: can't save data")
            return False
        print("succes ETL data !")
        return True
        
    except Exception as e:
        print(f"\nError during the process ETL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_etl_pipeline()
    sys.exit(0 if success else 1)
