import re
from .data_normalization import normalize_date, compute_check_digit, COUNTRY_CODES, GENDER
from .text_extraction import extract_text_from_roi, extract_text_from_roi_mrz
from .image_processing import extract_roi, extract_roi_mrz

def parse_mrz(image, mrz_roi):
    mrz_info = {}
    mrz_image = extract_roi_mrz(image, mrz_roi)
    text = extract_text_from_roi_mrz(mrz_image)
    
    print("Văn bản trích xuất từ MRZ:")
    print(repr(text)) 
    lines = text.splitlines()
    lines = [line.replace(" ", "").strip() for line in lines]
    mrz_lines = [line for line in lines if re.match(r'^P|^[A-Z0-9<]{44}$', line)]

    if len(mrz_lines) < 2:
        raise ValueError("Không tìm thấy đủ thông tin MRZ.")

    line1, line2 = mrz_lines[:2]
    if len(line1) < 44 or len(line2) < 44:
        raise ValueError("Dòng MRZ không đúng định dạng hoặc thiếu ký tự.")

    mrz_info['Loại'] = line1[0]
    mrz_info['Quốc gia'] = COUNTRY_CODES.get(line1[2:5], line1[2:5])
    mrz_info['Tên (tiếng Anh)'] = ' '.join([n.replace('<', ' ') for n in line1[5:44].split('<<')]).strip()
    mrz_info['Số hộ chiếu'] = line2[0:9].replace('<', '')
    mrz_info['Quốc tịch'] = COUNTRY_CODES.get(line2[10:13], line2[10:13])
    mrz_info['Ngày sinh'] = normalize_date(line2[13:19])
    mrz_info['Giới tính'] = GENDER.get(line2[20], 'U')
    mrz_info['Ngày hết hạn'] = normalize_date(line2[21:27])
    mrz_info['Số định danh cá nhân'] = line2[28:42].replace('<', '')

    # Validate check digit
    check_digit = compute_check_digit(line2[0:10] + line2[13:20] + line2[21:43])
    if check_digit != line2[43]:
        print("Cảnh báo: Check digit MRZ không khớp, thông tin có thể không chính xác.")

    return mrz_info