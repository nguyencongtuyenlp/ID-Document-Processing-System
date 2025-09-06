import cv2
import numpy as np

def preprocess_image(image):
    if image is None:
        raise ValueError("Không thể đọc ảnh")
    # Giữ nguyên màu sắc, chỉ resize
    image = cv2.resize(image, (590, 408), interpolation=cv2.INTER_LANCZOS4)
    return image

def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def enhance_contrast(image):
    # Giảm độ tương phản để ảnh tự nhiên hơn
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def extract_roi(image, roi):
    if image is None:
        raise ValueError("Không thể đọc ảnh")
    image = cv2.resize(image, (590, 408), interpolation=cv2.INTER_LANCZOS4)
    # Giữ nguyên màu sắc cho ROI
    x, y, w, h = roi
    cropped = image[y:y+h, x:x+w]
    resized = cv2.resize(cropped, None, fx=5, fy=5, interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite("final_image.jpg", resized)
    return resized

def extract_roi_mrz(image, roi):
    if image is None:
        raise ValueError("Không thể đọc ảnh")
    image = cv2.resize(image, (590, 408), interpolation=cv2.INTER_LANCZOS4)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x, y, w, h = roi
    cropped = image[y:y+h, x:x+w]
    resized = cv2.resize(cropped, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
    # Tắt enhance_contrast để ảnh tự nhiên hơn
    # enhanced = enhance_contrast(resized)
    # sharpened = sharpen_image(enhanced)
    # cv2.imwrite("final_MRZ.jpg", sharpened)
    # return sharpened
    cv2.imwrite("final_MRZ.jpg", resized)
    return resized

def scan_document1(reference_image, scanned_image):
    PARAMS = {
        "MAX_NUM_FEATURES": 10000,
        "GOOD_MATCH_PERCENT": 0.05,
        "RANSAC_REPROJ_THRESHOLD": 5.0,
        "ORB_SCALE_FACTOR": 1.2,
        "ORB_NLEVELS": 8,
        "OUTPUT_SIZE_SCALE": 1.0
    }

    im1 = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
    im2 = cv2.cvtColor(scanned_image, cv2.COLOR_BGR2RGB)

    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(
        nfeatures=PARAMS["MAX_NUM_FEATURES"],
        scaleFactor=PARAMS["ORB_SCALE_FACTOR"],
        nlevels=PARAMS["ORB_NLEVELS"]
    )
    kp1, des1 = orb.detectAndCompute(im1_gray, None)
    kp2, des2 = orb.detectAndCompute(im2_gray, None)

    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(des1, des2, None)
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = matches[:int(len(matches) * PARAMS["GOOD_MATCH_PERCENT"])]

    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

    for i, match in enumerate(good_matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt

    h, mask = cv2.findHomography(points2, points1, cv2.RANSAC, PARAMS["RANSAC_REPROJ_THRESHOLD"])
    height, width, _ = im1.shape
    im2_reg = cv2.warpPerspective(im2, h, (int(width * PARAMS["OUTPUT_SIZE_SCALE"]), int(height * PARAMS["OUTPUT_SIZE_SCALE"])))
    return cv2.cvtColor(im2_reg, cv2.COLOR_RGB2BGR)
