import pandas as pd
import os
from datetime import datetime

def create_output_directory():
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def load_to_csv(df, filename, output_dir='output'):
    if df is None or df.empty:
        print(f"No data save in{filename}")
        return False
    
    create_output_directory()
    filepath = os.path.join(output_dir, filename)
    
    try:
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f" {filepath}")
        print(f"  - rows: {len(df)}")
        print(f"  - cols: {len(df.columns)}")
        return True
    except Exception as e:
        print(f"error save file {filepath}: {str(e)}")
        return False

def load_to_parquet(df, filename, output_dir='output'):
    if df is None or df.empty:
        print(f"no data save in {filename}")
        return False
    
    create_output_directory()
    filepath = os.path.join(output_dir, filename)
    
    try:
        df.to_parquet(filepath, index=False, engine='pyarrow')
        print(f"saved sate {filepath}")
        print(f"  - rows: {len(df)}")
        print(f"  - cols: {len(df.columns)}")
        return True
    except Exception as e:
        print(f"error save file{filepath}: {str(e)}")
        return False

def load_to_json(df, filename, output_dir='output'):
    if df is None or df.empty:
        print(f"no data save in {filename}")
        return False
    
    create_output_directory()
    filepath = os.path.join(output_dir, filename)
    
    try:
        df.to_json(filepath, orient='records', indent=2, force_ascii=False)
        print(f"save data in{filepath}")
        print(f"  - rows: {len(df)}")
        print(f"  - cols: {len(df.columns)}")
        return True
    except Exception as e:
        print(f"error save data in {filepath}: {str(e)}")
        return False

def load_transformed_data(df_transformed, label_encoders=None):
    if df_transformed is None or df_transformed.empty:
        print("no data")
        return False
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    success_csv = load_to_csv(df_transformed, f'transformed_data_{timestamp}.csv')
    success_json = load_to_json(df_transformed, f'transformed_data_{timestamp}.json')
    

    if success_csv:
        stats = df_transformed.describe()
        load_to_csv(stats, f'data_statistics_{timestamp}.csv')
    
    if label_encoders:
        import json
        encoders_info = {}
        for col, encoder in label_encoders.items():
            encoders_info[col] = {
                'classes': encoder.classes_.tolist()
            }
        
        output_dir = create_output_directory()
        encoder_file = os.path.join(output_dir, f'label_encoders_{timestamp}.json')
        with open(encoder_file, 'w', encoding='utf-8') as f:
            json.dump(encoders_info, f, indent=2, ensure_ascii=False)
        print(f"save label encoders in {encoder_file}")
    return True
