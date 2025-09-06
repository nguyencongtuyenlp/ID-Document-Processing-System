# 🚀 Hướng dẫn Deploy Passport Reader

## 📋 Tổng quan

Dự án Passport Reader có 2 cách chạy chính:
1. **Streamlit App** - Giao diện đẹp, dễ sử dụng
2. **Web Server** - Giao diện chuyên nghiệp với API

## 🛠️ Cài đặt

### 1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 2. Cài đặt Tesseract OCR
- **Windows**: Tải từ [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 🚀 Cách chạy

### 1. Streamlit App (Khuyến nghị)
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```
- **URL**: http://localhost:8501
- **iPhone**: http://192.168.x.x:8501

### 2. Web Server (Chuyên nghiệp)
```bash
python web_server.py
```
- **URL**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/docs

## 📱 Truy cập từ điện thoại

### Sử dụng Ngrok (Khuyến nghị)
```bash
# Cài đặt ngrok
# Windows: tải từ https://ngrok.com/download
# Mac: brew install ngrok
# Linux: snap install ngrok

# Lấy auth token từ https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_TOKEN

# Tạo tunnel cho Streamlit
ngrok http 8501

# Tạo tunnel cho Web Server
ngrok http 8080
```

## ☁️ Deploy lên Cloud

### 1. Streamlit Cloud (Khuyến nghị)
1. Push code lên GitHub
2. Truy cập https://share.streamlit.io
3. Connect repository
4. Chọn file `streamlit_app.py`
5. Deploy

### 2. Heroku
```bash
# Tạo Procfile
echo "web: uvicorn web_server:app --host 0.0.0.0 --port $PORT" > Procfile

# Tạo runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 3. VPS (Ubuntu/Debian)
```bash
# Cài đặt dependencies
sudo apt update
sudo apt install python3-pip nginx tesseract-ocr

# Clone repository
git clone <your-repo>
cd passport_reader

# Cài đặt Python packages
pip3 install -r requirements.txt

# Chạy Streamlit
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## 🐛 Troubleshooting

### Lỗi thường gặp

1. **Tesseract not found**
   ```bash
   # Windows: Thêm vào PATH
   # Hoặc set trong code
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

2. **Port đã được sử dụng**
   ```bash
   # Tìm process sử dụng port
   netstat -ano | findstr :8501
   # Kill process
   taskkill /PID <PID> /F
   ```

3. **iPhone không vào được**
   - Đảm bảo dùng `--server.address 0.0.0.0`
   - Kiểm tra firewall
   - Dùng ngrok nếu cần

## 📞 Support

Nếu gặp vấn đề, hãy:
1. Kiểm tra logs
2. Test với ảnh mẫu
3. Kiểm tra dependencies
4. Tạo issue trên GitHub
