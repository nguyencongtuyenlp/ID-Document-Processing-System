import os
import cv2
import argparse
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
from src.text_extraction import extract_text_from_roi
from src.image_processing import preprocess_image, extract_roi, scan_document1
from src.mrz_parser import parse_mrz
from src.data_normalization import correct_place_of_birth, compare_names
from src.config import ROIS, MRZ_ROI

# Set đường dẫn Tesseract cho Windows
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Set TESSDATA_PREFIX
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

def try_parse_mrz(image):
    try:
        return parse_mrz(image, MRZ_ROI)
    except Exception as e:
        print(f"[MRZ] Không đọc được MRZ: {e}")
        return None

def detect_document_type(image):
    """Phát hiện loại tài liệu: CCCD hoặc Passport"""
    # Thử đọc text để phát hiện CCCD
    text = extract_text_from_roi(image)
    if "CĂN CƯỚC CÔNG DÂN" in text.upper():
        return "CCCD"
    
    # Thử parse MRZ để phát hiện Passport
    try:
        parse_mrz(image, MRZ_ROI)
        return "PASSPORT"
    except:
        return "CCCD"  # Mặc định là CCCD

def visualize_roi_detection(image, rois, title="ROI Detection"):
    """Hiển thị các vùng ROI được phát hiện"""
    image_copy = image.copy()
    
    # Vẽ các vùng ROI
    for i, roi in enumerate(rois, 1):
        x, y, w, h = roi
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image_copy, f"ROI {i}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Chuyển đổi màu từ BGR sang RGB cho matplotlib
    image_rgb = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(15, 10))
    plt.imshow(image_rgb)
    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.jpg", dpi=150, bbox_inches='tight')
    plt.show()

def visualize_feature_matching(ref_image, scan_image, title="Feature Matching"):
    """Hiển thị feature matching giữa 2 ảnh"""
    # Chuyển đổi màu
    ref_rgb = cv2.cvtColor(ref_image, cv2.COLOR_BGR2RGB)
    scan_rgb = cv2.cvtColor(scan_image, cv2.COLOR_BGR2RGB)
    
    # Detect ORB features
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(ref_image, None)
    kp2, des2 = orb.detectAndCompute(scan_image, None)
    
    # Match features
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # Draw matches
    good_matches = matches[:50]  # Top 50 matches
    img_matches = cv2.drawMatches(ref_image, kp1, scan_image, kp2, good_matches, None)
    img_matches_rgb = cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(20, 10))
    plt.imshow(img_matches_rgb)
    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.jpg", dpi=150, bbox_inches='tight')
    plt.show()

def visualize_processing_steps(original, processed, title="Processing Steps"):
    """Hiển thị các bước xử lý"""
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
    
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(original_rgb)
    plt.title("Original Image", fontsize=14)
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(processed_rgb)
    plt.title("Processed Image", fontsize=14)
    plt.axis('off')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.jpg", dpi=150, bbox_inches='tight')
    plt.show()

def main(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh tại: {image_path}")

    print(f"Đang xử lý: {image_path}")
    
    image = cv2.imread(image_path)
    cv2.imwrite("anh_goc.jpg", image)
    
    # Phát hiện loại tài liệu
    doc_type = detect_document_type(image)
    print(f"Loại tài liệu: {doc_type}")
    
    # Xử lý dựa trên loại tài liệu
    if doc_type == "PASSPORT":
        # Xử lý Passport
        form = cv2.imread("template/ho_chieu.jpg")
        mrz_info = try_parse_mrz(image)
        
        if mrz_info is None:
            print("[MRZ] Đang thử căn chỉnh ảnh...")
            if form is not None:
                image = scan_document1(form, image)
                cv2.imwrite("after_scan.jpg", image)
            mrz_info = try_parse_mrz(image)
            if mrz_info is None:
                raise ValueError("❌ Không thể trích xuất thông tin MRZ sau khi đã căn chỉnh.")
        
        preprocessed_img = preprocess_image(image)
        cv2.imwrite("temp_processed.jpg", preprocessed_img)
        
        for i, roi in enumerate(ROIS, start=1):
            roi_image = extract_roi(image, roi)
            output_path = f"{i}.jpg"
            cv2.imwrite(output_path, roi_image)
            extracted_text = extract_text_from_roi(roi_image)
            if i == 1 and isinstance(extracted_text, str) and extracted_text.strip():
                if compare_names(mrz_info.get('Tên (tiếng Anh)', '').strip(), extracted_text.strip()):
                    mrz_info['Tên (tiếng Anh)'] = extracted_text.strip()
            elif i == 2 and extracted_text:
                corrected_text = correct_place_of_birth(extracted_text)
                mrz_info['Nơi sinh'] = corrected_text
            elif i == 3 and extracted_text:
                mrz_info['Nơi cấp'] = extracted_text
            elif i == 4 and extracted_text:
                if compare_names(mrz_info.get('Tên (tiếng Anh)', '').strip(), extracted_text.strip()):
                    mrz_info['Tên (tiếng Anh)'] = extracted_text.strip()
        
        print("\nThông tin hộ chiếu:")
        for k, v in mrz_info.items():
            print(f"  {k}: {v}")
    
    else:  # CCCD
        # Xử lý CCCD
        from src.config import CCCD_ROIS
        form = cv2.imread("template/CCCD.png")
        
        print("🔍 Hiển thị quá trình xử lý CCCD...")
        
        # 1. Hiển thị ảnh gốc và template
        if form is not None:
            visualize_processing_steps(image, form, "Original vs Template")
            
            # 2. Hiển thị feature matching
            visualize_feature_matching(form, image, "Feature Matching - CCCD")
            
            # 3. Căn chỉnh ảnh
            print("📐 Đang căn chỉnh ảnh...")
            aligned_image = scan_document1(form, image)
            cv2.imwrite("after_scan.jpg", aligned_image)
            
            # 4. Hiển thị trước và sau căn chỉnh
            visualize_processing_steps(image, aligned_image, "Before vs After Alignment")
            image = aligned_image
        
        # 5. Hiển thị ROI detection
        print("🎯 Phát hiện các vùng ROI...")
        visualize_roi_detection(image, CCCD_ROIS, "CCCD ROI Detection")
        
        # 6. Xử lý ảnh
        preprocessed_img = preprocess_image(image)
        cv2.imwrite("temp_processed.jpg", preprocessed_img)
        
        # 7. Trích xuất thông tin từng ROI
        print("📝 Trích xuất thông tin từ các vùng ROI...")
        cccd_info = {}
        for i, roi in enumerate(CCCD_ROIS, start=1):
            roi_image = extract_roi(image, roi)
            output_path = f"roi_{i}.jpg"
            cv2.imwrite(output_path, roi_image)
            extracted_text = extract_text_from_roi(roi_image)
            if extracted_text:
                if i == 1:
                    cccd_info['Họ và tên'] = extracted_text
                elif i == 2:
                    cccd_info['Ngày sinh'] = extracted_text
                elif i == 3:
                    cccd_info['Nơi thường trú'] = extracted_text
                elif i == 4:
                    cccd_info['Nơi đăng ký thường trú'] = extracted_text
                print(f"  ROI {i}: {extracted_text}")
        
        print("\n✅ Thông tin CCCD đã trích xuất:")
        for k, v in cccd_info.items():
            print(f"  {k}: {v}")
        
        print("\n📁 Các file đã tạo:")
        print("  - roi_1.jpg, roi_2.jpg, roi_3.jpg, roi_4.jpg (các vùng ROI)")
        print("  - after_scan.jpg (ảnh sau căn chỉnh)")
        print("  - temp_processed.jpg (ảnh đã xử lý)")
        print("  - feature_matching_-_cccd.jpg (feature matching)")
        print("  - cccd_roi_detection.jpg (phát hiện ROI)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Passport Reader")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn ảnh input")
    args = parser.parse_args()
    try:
        main(args.image)
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")