"""
File cấu hình cho ETL pipeline
"""
import os

# Đường dẫn dữ liệu
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

# Tên các file dữ liệu
DATA_FILES = {
    'ev2023': 'data/Cheapestelectriccars_EVDatabase2023.csv',
    'ev2024': 'data/Cheapestelectriccars_EVDatabase.csv',
    'ev2025': 'data/electric_vehicles_spec_2025.csv'
}

# Cấu hình cho Transform
TRANSFORM_CONFIG = {
    'outlier_contamination': 0.1,  # Tỷ lệ outliers dự kiến
    'knn_neighbors': 5,  # Số neighbors cho KNN imputation
    'remove_outliers': False,  # Có loại bỏ outliers hay không
}

# Cấu hình cho Clustering
CLUSTERING_CONFIG = {
    'n_clusters': 4,  # Số cụm cho K-Means
    'random_state': 42,
}

# Cấu hình cho Model Prediction
MODEL_CONFIG = {
    'test_size': 0.2,  # Tỷ lệ dữ liệu test
    'random_state': 42,
    'n_estimators': 100,  # Số trees cho Random Forest
    'max_depth': 10,
}

# Các cột số cần làm sạch
NUMERIC_COLUMNS = [
    'Acceleration',
    'TopSpeed',
    'Range',
    'Efficiency',
    'FastChargeSpeed',
    'PriceinGermany',
    'PriceinUK',
    'NumberofSeats'
]

# Đơn vị cần loại bỏ cho từng cột
UNIT_REMOVAL = {
    'Acceleration': 'sec',
    'TopSpeed': 'km/h',
    'Range': 'km',
    'Efficiency': 'Wh/km',
    'FastChargeSpeed': 'km/h',
}

# Tạo thư mục output nếu chưa tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)
