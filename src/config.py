provinces = [
    "An Giang", "Bà Rịa - Vũng Tàu", "Bạc Liêu", "Bắc Giang", "Bắc Kạn", "Bắc Ninh",
    "Bến Tre", "Bình Dương", "Bình Định", "Bình Phước", "Bình Thuận", "Cà Mau",
    "Cao Bằng", "Cần Thơ", "Đà Nẵng", "Đắk Lắk", "Đắk Nông", "Điện Biên", "Đồng Nai",
    "Đồng Tháp", "Gia Lai", "Hà Giang", "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương",
    "Hải Phòng", "Hậu Giang", "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang",
    "Kon Tum", "Lai Châu", "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định",
    "Nghệ An", "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình",
    "Quảng Nam", "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La",
    "Tây Ninh", "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang",
    "Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái"
]

# ROI cho CCCD
CCCD_ROIS = [
    (150, 150, 250, 30),  # Họ và tên (ước lượng, cần điều chỉnh)
    (150, 200, 200, 30),  # Ngày sinh
    (150, 250, 200, 30),  # Nơi thường trú (ước lượng)
    (150, 300, 200, 30),  # Nơi đăng ký thường trú (ước lượng)
]

# ROI cho Hộ chiếu (giữ nguyên ROIS cũ)
ROIS = [
    (200, 101, 264, 24),  # Tên cũ
    (382, 156, 151, 27),  # Nơi sinh
    (203, 269, 237, 29),  # Nơi cấp
    (224, 107, 334, 23)   # Tên mới
]

# Vùng ROI cho MRZ (chỉ áp dụng cho Hộ chiếu)
MRZ_ROI = (0, 311, 590, 97)

# Loại tài liệu
DOCUMENT_TYPES = {
    "CCCD": {"rois": CCCD_ROIS, "has_mrz": False},
    "PASSPORT": {"rois": ROIS, "has_mrz": True}
}