# 📄 Passport Reader - Hệ thống đọc giấy tờ tùy thân thông minh

## 🎯 Tính năng chính

- ✅ **Đọc Hộ chiếu Việt Nam** - Trích xuất thông tin từ MRZ và các vùng ROI
- ✅ **Đọc CCCD mới** - Nhận diện và đọc thông tin căn cước công dân
- ✅ **Tự động phát hiện** - Phân biệt loại tài liệu tự động
- ✅ **Căn chỉnh ảnh** - Tự động căn chỉnh ảnh với template
- ✅ **Giao diện đa dạng** - Web App, Streamlit, API
- ✅ **Camera support** - Chụp ảnh trực tiếp từ điện thoại

## 🚀 Cài đặt nhanh

### 1. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### 2. Cài đặt Tesseract OCR:
- **Windows**: Tải từ [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 🎮 Cách chạy

### 🌐 Web App (Khuyến nghị cho demo HR):
```bash
python web_server.py
# Truy cập: http://localhost:8080
```

### 📱 Streamlit App (Giao diện đẹp):
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
# Truy cập: http://localhost:8501
```

### 📱 Truy cập từ điện thoại:
```bash
# Cài đặt ngrok
ngrok config add-authtoken YOUR_TOKEN

# Tạo tunnel
ngrok http 8501  # Cho streamlit
# hoặc
ngrok http 8080  # Cho web app
```

## 📁 Cấu trúc dự án

```
passport_reader/
├── 🌐 web_server.py          # Web server chính (FastAPI)
├── 📱 streamlit_app.py       # Streamlit app (giao diện đẹp)
├── 🖥️ main.py               # CLI interface
├── 📋 requirements.txt       # Dependencies
├── 📖 DEPLOYMENT.md         # Hướng dẫn deploy chi tiết
├── 📁 src/                  # Source code
│   ├── config.py            # Cấu hình ROI
│   ├── image_processing.py  # Xử lý ảnh
│   ├── text_extraction.py   # OCR
│   ├── mrz_parser.py        # Parse MRZ
│   └── data_normalization.py # Chuẩn hóa dữ liệu
├── 📁 templates/            # Web frontend
│   └── index.html           # Giao diện web
├── 📁 static/               # Static files
└── 📁 template/             # Template images
    ├── CCCD.png
    └── ho_chieu.jpg
```

## 🎨 Giao diện

### 🌐 Web App (Chuyên nghiệp)
- 🎨 Giao diện hiện đại với gradient và animations
- 📱 Responsive design cho mobile
- 📸 Camera upload và drag & drop
- 🖼️ Gallery hiển thị ảnh đã xử lý
- 📊 Thông tin được hiển thị dạng cards đẹp mắt

### 📱 Streamlit App (Đơn giản)
- ⚙️ Sidebar với cài đặt chi tiết
- 📊 Metrics và thống kê
- 🎯 Tự động phát hiện loại tài liệu
- 💾 Tải xuống ảnh đã xử lý

## 🚀 Deploy lên Cloud

### Streamlit Cloud (Khuyến nghị)
1. Push code lên GitHub
2. Truy cập https://share.streamlit.io
3. Connect repository và deploy

### Heroku
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### VPS
Xem chi tiết trong `DEPLOYMENT.md`

## 🛠️ Công nghệ sử dụng

- **Backend**: FastAPI, OpenCV, Tesseract OCR
- **Frontend**: HTML5, CSS3, JavaScript, Streamlit
- **AI/ML**: Computer Vision, OCR, Image Processing
- **Deploy**: Heroku, Streamlit Cloud, VPS

## 📞 Liên hệ

Dự án được phát triển để demo kỹ năng lập trình và AI/ML cho HR! 🚀