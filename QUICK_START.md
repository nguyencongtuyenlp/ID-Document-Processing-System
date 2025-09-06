# 🚀 Quick Start - Passport Reader

## ⚡ Chạy nhanh trong 30 giây

### 1. Cài đặt
```bash
# Kích hoạt môi trường ảo
& "d:/Project github/passport_reader (5)/passport_reader/.venv/Scripts/Activate.ps1"

# Cài đặt thư viện
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

#### 📱 Streamlit (Khuyến nghị)
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```
- **Máy tính**: http://localhost:8501
- **iPhone**: http://192.168.x.x:8501

#### 🌐 Web Server
```bash
python web_server.py
```
- **Máy tính**: http://localhost:8080
- **iPhone**: http://192.168.x.x:8080

### 3. Test nhanh
1. Mở trình duyệt
2. Upload ảnh CCCD/Passport
3. Xem kết quả trích xuất

## 🎯 Demo cho HR

### Điểm nổi bật:
- ✅ **Giao diện đẹp** - Modern UI với animations
- ✅ **Camera support** - Chụp ảnh trực tiếp từ iPhone
- ✅ **Tự động phát hiện** - Nhận diện CCCD/Passport
- ✅ **Căn chỉnh ảnh** - Tự động căn chỉnh với template
- ✅ **OCR thông minh** - Trích xuất thông tin chính xác
- ✅ **Responsive** - Hoạt động tốt trên mọi thiết bị

### Công nghệ:
- **AI/ML**: Computer Vision, OCR, Image Processing
- **Backend**: Python, FastAPI, OpenCV, Tesseract
- **Frontend**: Streamlit, HTML5, CSS3, JavaScript
- **Deploy**: Streamlit Cloud, Heroku, VPS

## 📞 Support
- **README.md**: Hướng dẫn chi tiết
- **DEPLOYMENT.md**: Hướng dẫn deploy
- **DEMO.md**: Hướng dẫn demo cho HR
