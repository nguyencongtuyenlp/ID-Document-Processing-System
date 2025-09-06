from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import os
import base64
import json
from PIL import Image
import io
from src.image_processing import preprocess_image, extract_roi, scan_document1
from src.text_extraction import extract_text_from_roi
from src.mrz_parser import parse_mrz
from src.data_normalization import correct_place_of_birth, compare_names
from src.config import CCCD_ROIS, ROIS, MRZ_ROI, DOCUMENT_TYPES

# Tạo app chính
app = FastAPI(
    title="Passport Reader Web App",
    description="Web app để đọc thông tin từ Hộ chiếu và CCCD",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tạo thư mục static nếu chưa có
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def detect_document_type(image):
    """Phát hiện loại tài liệu: CCCD hoặc Passport"""
    try:
        text = extract_text_from_roi(image)
        if "CĂN CƯỚC CÔNG DÂN" in text.upper():
            return "CCCD"
        
        # Thử parse MRZ để phát hiện Passport
        try:
            parse_mrz(image, MRZ_ROI)
            return "PASSPORT"
        except:
            return "CCCD"  # Mặc định là CCCD
    except:
        return "CCCD"

def process_image_file(file_content):
    """Xử lý file ảnh từ upload"""
    try:
        # Chuyển đổi bytes thành numpy array
        nparr = np.frombuffer(file_content, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Không thể đọc ảnh")
        
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý ảnh: {str(e)}")

def save_processed_images(image, doc_type, rois):
    """Lưu các ảnh đã xử lý"""
    saved_files = {}
    
    # Lưu ảnh gốc
    cv2.imwrite("static/original.jpg", image)
    saved_files["original"] = "static/original.jpg"
    
    # Lưu ảnh đã xử lý
    preprocessed = preprocess_image(image)
    cv2.imwrite("static/processed.jpg", preprocessed)
    saved_files["processed"] = "static/processed.jpg"
    
    # Lưu các ROI
    for i, roi in enumerate(rois, 1):
        roi_image = extract_roi(image, roi)
        roi_path = f"static/roi_{i}.jpg"
        cv2.imwrite(roi_path, roi_image)
        saved_files[f"roi_{i}"] = roi_path
    
    return saved_files

# Serve frontend
@app.get("/")
async def read_index():
    return FileResponse("templates/index.html")

@app.get("/health")
async def health():
    return {"status": "OK", "message": "Web app is running"}

@app.post("/api/process-document")
async def process_document(file: UploadFile = File(...)):
    """Xử lý ảnh passport/CCCD và trả về thông tin"""
    try:
        # Đọc file ảnh
        file_content = await file.read()
        image = process_image_file(file_content)
        
        # Phát hiện loại tài liệu
        doc_type = detect_document_type(image)
        
        # Lấy template và căn chỉnh ảnh
        template_path = "template/CCCD.png" if doc_type == "CCCD" else "template/ho_chieu.jpg"
        form = cv2.imread(template_path)
        
        if form is not None:
            try:
                image = scan_document1(form, image)
                cv2.imwrite("static/aligned.jpg", image)
            except Exception as e:
                print(f"Cảnh báo: Không thể căn chỉnh ảnh: {e}")
        
        # Lấy cấu hình ROI
        rois = DOCUMENT_TYPES[doc_type]["rois"]
        has_mrz = DOCUMENT_TYPES[doc_type]["has_mrz"]
        
        # Lưu các ảnh đã xử lý
        saved_files = save_processed_images(image, doc_type, rois)
        
        # Trích xuất thông tin
        info = {}
        
        # Xử lý MRZ cho hộ chiếu
        if has_mrz:
            try:
                mrz_info = parse_mrz(image, MRZ_ROI)
                info.update(mrz_info)
            except Exception as e:
                print(f"Cảnh báo: Không thể đọc MRZ: {e}")
        
        # Trích xuất thông tin từ các ROI
        for i, roi in enumerate(rois, 1):
            try:
                roi_image = extract_roi(image, roi)
                extracted_text = extract_text_from_roi(roi_image)
                
                if extracted_text:
                    if doc_type == "CCCD":
                        if i == 1:
                            info['Họ và tên'] = extracted_text
                        elif i == 2:
                            info['Ngày sinh'] = extracted_text
                        elif i == 3:
                            info['Nơi thường trú'] = extracted_text
                        elif i == 4:
                            info['Nơi đăng ký thường trú'] = extracted_text
                    elif doc_type == "PASSPORT":
                        if i == 1 and compare_names(info.get('Tên (tiếng Anh)', '').strip(), extracted_text.strip()):
                            info['Tên (tiếng Anh)'] = extracted_text.strip()
                        elif i == 2:
                            corrected_text = correct_place_of_birth(extracted_text)
                            info['Nơi sinh'] = corrected_text
                        elif i == 3:
                            info['Nơi cấp'] = extracted_text
                        elif i == 4 and compare_names(info.get('Tên (tiếng Anh)', '').strip(), extracted_text.strip()):
                            info['Tên (tiếng Anh)'] = extracted_text.strip()
            except Exception as e:
                print(f"Cảnh báo: Lỗi xử lý ROI {i}: {e}")
        
        return {
            "success": True,
            "document_type": doc_type,
            "extracted_info": info,
            "processed_images": saved_files,
            "message": f"Đã xử lý thành công {doc_type}"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Lỗi xử lý tài liệu"
            }
        )

@app.get("/api/images/{filename}")
async def get_image(filename: str):
    """Lấy ảnh đã xử lý"""
    file_path = f"static/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")

@app.get("/api/health")
async def api_health():
    """Kiểm tra sức khỏe API"""
    return {
        "status": "healthy",
        "message": "API đang hoạt động bình thường",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Passport Reader Web Server...")
    print("📱 Web App: http://localhost:8080")
    print("🔌 API Docs: http://localhost:8080/api/docs")
    print("❤️ Health Check: http://localhost:8080/health")
    uvicorn.run(app, host="127.0.0.1", port=8080)
