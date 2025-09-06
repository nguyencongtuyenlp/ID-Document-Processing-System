# 🎯 Hướng dẫn Demo Passport Reader

## 🚀 Demo nhanh cho HR

### 1. Chuẩn bị
```bash
# Kích hoạt môi trường ảo
& "d:/Project github/passport_reader (5)/passport_reader/.venv/Scripts/Activate.ps1"

# Cài đặt thư viện (nếu chưa có)
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

#### 📱 Streamlit (Khuyến nghị cho demo)
```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```
- **Máy tính**: http://localhost:8501
- **iPhone**: http://192.168.x.x:8501

#### 🌐 Web Server (Chuyên nghiệp)
```bash
python web_server.py
```
- **Máy tính**: http://localhost:8080
- **iPhone**: http://192.168.x.x:8080

### 3. Demo cho HR

#### ✨ Điểm nổi bật:
- **Giao diện đẹp** - Modern UI với gradient và animations
- **Camera support** - Chụp ảnh trực tiếp từ iPhone
- **Tự động phát hiện** - Nhận diện CCCD/Passport tự động
- **Căn chỉnh ảnh** - Tự động căn chỉnh với template
- **OCR thông minh** - Trích xuất thông tin chính xác
- **Responsive** - Hoạt động tốt trên mọi thiết bị

#### 🎯 Quy trình demo:
1. Mở ứng dụng trên máy tính
2. Chụp ảnh CCCD/Passport bằng iPhone
3. Xem quá trình xử lý real-time
4. Kiểm tra kết quả trích xuất
5. Tải xuống ảnh đã xử lý

### 4. Truy cập từ iPhone

#### Cách 1: Mạng LAN
- Đảm bảo iPhone và máy tính cùng mạng WiFi
- Tìm IP máy tính: `ipconfig`
- Truy cập: `http://IP_MÁY_TÍNH:8501`

#### Cách 2: Ngrok (Nếu cần)
```bash
# Cài đặt ngrok
ngrok config add-authtoken YOUR_TOKEN

# Tạo tunnel
ngrok http 8501
```

### 5. Troubleshooting

#### Lỗi thường gặp:
- **iPhone không vào được**: Dùng `--server.address 0.0.0.0`
- **Tesseract not found**: Cài đặt Tesseract OCR
- **Port bị chiếm**: Đổi port khác

#### Kiểm tra:
```bash
# Kiểm tra port
netstat -ano | findstr :8501

# Kiểm tra IP
ipconfig
```

## 🎉 Chúc demo thành công!
