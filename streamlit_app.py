import streamlit as st
import cv2
import numpy as np
import os
import tempfile
from PIL import Image
import base64
from src.image_processing import preprocess_image, extract_roi, scan_document1
from src.text_extraction import extract_text_from_roi
from src.mrz_parser import parse_mrz
from src.data_normalization import correct_place_of_birth, compare_names
from src.config import CCCD_ROIS, ROIS, MRZ_ROI, DOCUMENT_TYPES

# Cấu hình trang
st.set_page_config(
    page_title="📄 Passport Reader",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .success-card {
        background: #f0fdf4;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    
    .error-card {
        background: #fef2f2;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #dc2626;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

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

def process_document(image, doc_type):
    """Xử lý tài liệu và trích xuất thông tin"""
    try:
        # Lấy template và căn chỉnh ảnh
        template_path = "template/CCCD.png" if doc_type == "CCCD" else "template/ho_chieu.jpg"
        form = cv2.imread(template_path)
        
        aligned_image = image
        if form is not None:
            try:
                aligned_image = scan_document1(form, image)
            except Exception as e:
                st.warning(f"Không thể căn chỉnh ảnh: {e}")
        
        # Lấy cấu hình ROI
        rois = DOCUMENT_TYPES[doc_type]["rois"]
        has_mrz = DOCUMENT_TYPES[doc_type]["has_mrz"]
        
        # Trích xuất thông tin
        info = {}
        
        # Xử lý MRZ cho hộ chiếu
        if has_mrz:
            try:
                mrz_info = parse_mrz(aligned_image, MRZ_ROI)
                info.update(mrz_info)
            except Exception as e:
                st.warning(f"Không thể đọc MRZ: {e}")
        
        # Trích xuất thông tin từ các ROI
        roi_images = []
        for i, roi in enumerate(rois, 1):
            try:
                roi_image = extract_roi(aligned_image, roi)
                roi_images.append(roi_image)
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
                st.warning(f"Lỗi xử lý ROI {i}: {e}")
                roi_images.append(None)
        
        return info, aligned_image, roi_images
        
    except Exception as e:
        st.error(f"Lỗi xử lý tài liệu: {e}")
        return {}, image, []

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📄 Passport Reader</h1>
        <p>Đọc thông tin từ Hộ chiếu và CCCD một cách thông minh</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Cài đặt")
        
        # Chọn loại tài liệu
        doc_type = st.selectbox(
            "Loại tài liệu",
            ["Tự động phát hiện", "CCCD", "Hộ chiếu"],
            help="Chọn loại tài liệu hoặc để tự động phát hiện"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Thống kê")
        if 'processed_count' not in st.session_state:
            st.session_state.processed_count = 0
        st.metric("Đã xử lý", st.session_state.processed_count)
        
        st.markdown("---")
        st.markdown("### ℹ️ Hướng dẫn")
        st.markdown("""
        1. **Tải lên ảnh** từ máy tính hoặc chụp từ camera
        2. **Chọn loại tài liệu** hoặc để tự động phát hiện
        3. **Xem kết quả** trích xuất thông tin
        4. **Tải xuống** ảnh đã xử lý nếu cần
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Tải lên ảnh")
        
        # Upload methods
        upload_method = st.radio(
            "Chọn phương thức:",
            ["Từ máy tính", "Chụp từ camera"],
            horizontal=True
        )
        
        uploaded_file = None
        
        if upload_method == "Từ máy tính":
            uploaded_file = st.file_uploader(
                "Chọn file ảnh",
                type=['jpg', 'jpeg', 'png'],
                help="Hỗ trợ định dạng JPG, PNG, JPEG"
            )
        else:
            # Camera input - Đơn giản hóa
            camera_file = st.camera_input("Chụp ảnh tài liệu")
            if camera_file:
                uploaded_file = camera_file
        
        # Process button
        process_btn = st.button("🚀 Xử lý tài liệu", type="primary", use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Kết quả")
        
        if uploaded_file is not None and process_btn:
            # Chuyển đổi file thành OpenCV image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if image is not None:
                # Phát hiện loại tài liệu
                if doc_type == "Tự động phát hiện":
                    detected_type = detect_document_type(image)
                    st.success(f"🎯 Đã phát hiện: **{detected_type}**")
                else:
                    detected_type = doc_type
                
                # Xử lý tài liệu
                with st.spinner("Đang xử lý tài liệu..."):
                    info, aligned_image, roi_images = process_document(image, detected_type)
                
                if info:
                    st.session_state.processed_count += 1
                    
                    # Hiển thị thông tin
                    st.markdown(f"""
                    <div class="success-card">
                        <h4>✅ Đã trích xuất thành công {len(info)} thông tin</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Hiển thị thông tin dạng metrics
                    for key, value in info.items():
                        st.metric(key, value or "N/A")
                    
                    # Hiển thị ảnh đã xử lý
                    st.markdown("### 🖼️ Ảnh đã xử lý")
                    
                    # Ảnh gốc và đã căn chỉnh
                    col_img1, col_img2 = st.columns(2)
                    
                    with col_img1:
                        st.image(image, caption="Ảnh gốc", use_container_width=True)
                    
                    with col_img2:
                        st.image(aligned_image, caption="Ảnh đã căn chỉnh", use_container_width=True)
                    
                    # Các vùng ROI
                    if roi_images:
                        st.markdown("### 🎯 Các vùng thông tin")
                        roi_cols = st.columns(2)
                        
                        for i, roi_img in enumerate(roi_images):
                            if roi_img is not None:
                                with roi_cols[i % 2]:
                                    st.image(roi_img, caption=f"Vùng {i+1}", use_container_width=True)
                    
                    # Tải xuống ảnh
                    st.markdown("### 💾 Tải xuống")
                    
                    # Chuyển đổi ảnh thành bytes để tải xuống
                    _, buffer = cv2.imencode('.jpg', aligned_image)
                    img_bytes = buffer.tobytes()
                    
                    st.download_button(
                        label="📥 Tải xuống ảnh đã xử lý",
                        data=img_bytes,
                        file_name=f"processed_{detected_type.lower()}.jpg",
                        mime="image/jpeg"
                    )
                    
                    # Hiển thị JSON kết quả
                    with st.expander("📄 Xem dữ liệu JSON"):
                        st.json(info)
                
                else:
                    st.markdown("""
                    <div class="error-card">
                        <h4>❌ Không thể trích xuất thông tin</h4>
                        <p>Vui lòng thử lại với ảnh rõ nét hơn hoặc kiểm tra loại tài liệu.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Không thể đọc ảnh. Vui lòng thử lại!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>📄 Passport Reader - Được phát triển với ❤️ bằng Python & Streamlit</p>
        <p>Hỗ trợ: Hộ chiếu Việt Nam, CCCD mới</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()