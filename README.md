# ETL Pipeline cho Dữ liệu Xe Điện

Dự án ETL (Extract, Transform, Load) với các thuật toán Machine Learning để xử lý và phân tích dữ liệu xe điện.

## Cấu trúc dự án

```
ETL-data_FlowerD1006/
├── data/                          # Thư mục chứa dữ liệu gốc
│   ├── Cheapestelectriccars_EVDatabase2023.csv
│   ├── Cheapestelectriccars_EVDatabase.csv
│   └── electric_vehicles_spec_2025.csv
├── output/                        # Thư mục chứa kết quả (tự động tạo)
├── extract.py                     # Module trích xuất dữ liệu
├── transform.py                   # Module biến đổi dữ liệu (có ML)
├── load.py                        # Module lưu dữ liệu
├── main.py                        # File chính chạy ETL pipeline
├── analysis.py                    # File phân tích dữ liệu với ML
├── config.py                      # File cấu hình
└── requirements.txt               # Các thư viện cần thiết
```

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

### 1. Chạy ETL Pipeline

Chạy toàn bộ luồng ETL (Extract → Transform → Load):

```bash
python main.py
```

Luồng ETL sẽ:
- **Extract**: Trích xuất dữ liệu từ các file CSV
- **Transform**: 
  - Làm sạch dữ liệu (loại bỏ đơn vị, ký tự đặc biệt)
  - Phát hiện outliers bằng Isolation Forest
  - Impute missing values bằng KNN
  - Feature engineering (tạo các features mới)
  - Mã hóa các biến phân loại
- **Load**: Lưu dữ liệu đã transform vào thư mục `output/`

### 2. Phân tích dữ liệu

Sau khi chạy ETL, bạn có thể phân tích dữ liệu:

```bash
python analysis.py
```

File `analysis.py` sẽ thực hiện:
- Thống kê mô tả
- Phân tích tương quan (correlation analysis)
- Phân tích phân phối
- Phân cụm dữ liệu bằng K-Means
- Xây dựng mô hình dự đoán giá bằng Random Forest
- Tạo báo cáo insights

## Các tính năng Machine Learning

### 1. Outlier Detection (Isolation Forest)
- Phát hiện các giá trị bất thường trong dữ liệu
- Có thể cấu hình tỷ lệ contamination trong `config.py`

### 2. Missing Value Imputation (KNN Imputer)
- Impute các giá trị thiếu bằng K-Nearest Neighbors
- Sử dụng StandardScaler để chuẩn hóa trước khi impute

### 3. Feature Engineering
- Tạo các features mới:
  - `AveragePrice`: Giá trung bình
  - `RangePerPrice`: Tỷ lệ tầm hoạt động/giá
  - `EnergyEfficiency`: Hiệu suất năng lượng
  - `SpeedCategory`: Phân loại tốc độ
  - `RangeCategory`: Phân loại tầm hoạt động
  - `PriceCategory`: Phân loại giá

### 4. Clustering (K-Means)
- Phân cụm xe điện dựa trên các đặc điểm
- Sử dụng PCA để visualization nếu có nhiều features

### 5. Price Prediction (Random Forest)
- Dự đoán giá xe điện dựa trên các đặc điểm kỹ thuật
- Đánh giá mô hình bằng R², MAE, RMSE
- Hiển thị feature importance

## Kết quả

Sau khi chạy, các file kết quả sẽ được lưu trong thư mục `output/`:

- `transformed_data_YYYYMMDD_HHMMSS.csv`: Dữ liệu đã transform
- `transformed_data_YYYYMMDD_HHMMSS.json`: Dữ liệu dạng JSON
- `data_statistics_YYYYMMDD_HHMMSS.csv`: Thống kê mô tả
- `label_encoders_YYYYMMDD_HHMMSS.json`: Thông tin label encoders
- `correlation_heatmap.png`: Biểu đồ tương quan
- `distribution_analysis.png`: Biểu đồ phân phối
- `clustering_analysis.png`: Biểu đồ phân cụm
- `price_prediction_model.png`: Kết quả mô hình dự đoán
- `insights_report.txt`: Báo cáo insights

## Cấu hình

Bạn có thể chỉnh sửa các tham số trong file `config.py`:
- `TRANSFORM_CONFIG`: Cấu hình cho transform
- `CLUSTERING_CONFIG`: Cấu hình cho clustering
- `MODEL_CONFIG`: Cấu hình cho mô hình prediction

## Yêu cầu hệ thống

- Python 3.7+
- Các thư viện trong `requirements.txt`

## Tác giả

Dự án ETL với Machine Learning cho dữ liệu xe điện.

