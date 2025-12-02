import pandas as pd
import numpy as np
import re
import warnings

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
from extract import extract_all_data
warnings.filterwarnings('ignore')

def clean_numeric_column(column_series, unit_remove):
    cleaned_series = column_series.astype(str)
    
    # remove unit
    if unit_remove:
        cleaned_series = cleaned_series.str.replace(re.escape(unit_remove), '', regex=True)
    
    cleaned_series = cleaned_series.str.replace('€', '', regex=False)
    cleaned_series = cleaned_series.str.replace('£', '', regex=False)
    cleaned_series = cleaned_series.str.replace(',', '', regex=False)
    cleaned_series = cleaned_series.replace(['-', 'nan', '', 'N/A', 'n/a'], np.nan)
    
    return pd.to_numeric(cleaned_series, errors='coerce')

def detect_outliers_isolation_forest(df, columns, contamination=0.1):
    outlier_df = df.copy()
    outlier_flags = pd.Series([False] * len(df), index=df.index)
    
    for col in columns:
        if col in df.columns and df[col].notna().sum() > 0:
            valid_data = df[[col]].dropna()
            if len(valid_data) > 10:  
                iso_forest = IsolationForest(contamination=contamination, random_state=42)
                outliers = iso_forest.fit_predict(valid_data)
                outlier_flags.loc[valid_data.index] = outliers == -1
    
    return outlier_flags

def impute_missing_values_knn(df, numeric_columns, n_neighbors=5):
    """KNN"""
    df_imputed = df.copy()
    
    cols_to_impute = [col for col in numeric_columns if col in df.columns]
    
    if len(cols_to_impute) > 0:
        scaler = StandardScaler()
        df_scaled = df[cols_to_impute].copy()
        df_scaled[cols_to_impute] = scaler.fit_transform(df_scaled[cols_to_impute].fillna(0))
        
        # KNN Imputer
        imputer = KNNImputer(n_neighbors=n_neighbors)
        imputed_data = imputer.fit_transform(df_scaled[cols_to_impute])
        
        imputed_data = scaler.inverse_transform(imputed_data)
        df_imputed[cols_to_impute] = imputed_data
    
    return df_imputed

def feature_engineering(df):
    df_fe = df.copy()
    price_cols = ['PriceinGermany', 'PriceinUK']
    df_fe['AveragePrice'] = df_fe[price_cols].mean(axis=1)
    
    
    if 'Range' in df_fe.columns and 'AveragePrice' in df_fe.columns:
        df_fe['RangePerPrice'] = df_fe['Range'] / (df_fe['AveragePrice'] + 1)  # +1 để tránh chia 0
    

    if 'Range' in df_fe.columns and 'Efficiency' in df_fe.columns:
        df_fe['EnergyEfficiency'] = df_fe['Range'] / (df_fe['Efficiency'] + 1)
    
    if 'TopSpeed' in df_fe.columns:
        df_fe['SpeedCategory'] = pd.cut(
            df_fe['TopSpeed'],
            bins=[0, 150, 200, 250, 1000],
            labels=['Slow', 'Medium', 'Fast', 'Very Fast']
        )
    
    if 'Range' in df_fe.columns:
        df_fe['RangeCategory'] = pd.cut(
            df_fe['Range'],
            bins=[0, 300, 400, 500, 1000],
            labels=['Short', 'Medium', 'Long', 'Very Long']
        )

    if 'AveragePrice' in df_fe.columns:
        df_fe['PriceCategory'] = pd.cut(
            df_fe['AveragePrice'],
            bins=[0, 50000, 100000, 150000, float('inf')],
            labels=['Budget', 'Mid-range', 'Premium', 'Luxury']
        )
    
    return df_fe

def encode_categorical_features(df):
    
    df_encoded = df.copy()
    label_encoders = {}
    
    categorical_cols = ['Drive', 'SpeedCategory', 'RangeCategory', 'PriceCategory']
    
    for col in categorical_cols:
        if col in df_encoded.columns:
            le = LabelEncoder()
            
            df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col].astype(str))
            label_encoders[col] = le
    
    return df_encoded, label_encoders

def transform_data():
    # 1. Extract
    try:
        df_ev2023, df_ev2024, df_ele = extract_all_data()
    except Exception as e:
        print(f"Lỗi khi gọi extract_all_data: {e}")
        return None, None
    
    if df_ev2023 is None or df_ev2024 is None:
        print("Lỗi: Không tìm thấy dữ liệu đầu vào.")
        return None, None
    
    print(f"   - Đã đọc {len(df_ev2023)} dòng từ EV2023 và {len(df_ev2024)} dòng từ EV2024")
    
    # 2.(Cleaning)
    dataframes_to_clean = [df_ev2023, df_ev2024]
    
    for df in dataframes_to_clean:
        df['Acceleration'] = clean_numeric_column(df['Acceleration'], 'sec')
        df['TopSpeed'] = clean_numeric_column(df['TopSpeed'], 'km/h')
        df['Range'] = clean_numeric_column(df['Range'], 'km')
        df['Efficiency'] = clean_numeric_column(df['Efficiency'], 'Wh/km')
        df['FastChargeSpeed'] = clean_numeric_column(df['FastChargeSpeed'], 'km/h')
        df['PriceinGermany'] = clean_numeric_column(df['PriceinGermany'], '')
        df['PriceinUK'] = clean_numeric_column(df['PriceinUK'], '')
        
        if 'NumberofSeats' in df.columns:
            df['NumberofSeats'] = clean_numeric_column(df['NumberofSeats'], '')
    
    # 3.(Combine & Deduplicate)
    df_combined = pd.concat([df_ev2023, df_ev2024], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=['Name'], keep='first')
    
    # 4. outliers
    numeric_cols = ['Acceleration', 'TopSpeed', 'Range', 'Efficiency', 
                    'FastChargeSpeed', 'PriceinGermany', 'PriceinUK']
    detect_outliers_isolation_forest(df_combined, numeric_cols)
    
    # 5. Impute missing values với KNN
    df_combined = impute_missing_values_knn(df_combined, numeric_cols)
    
    # 6. Feature engineering
    df_combined = feature_engineering(df_combined)
    
    # 7. Encode categorical features
    df_combined, label_encoders = encode_categorical_features(df_combined)
    return df_combined, label_encoders

