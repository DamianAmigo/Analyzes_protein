import cv2

def procesar(image_path, blockSize=23, C=-1):
    """Applies adaptive thresholding with GAUSSIAN_C followed by Otsu and performs intersection with the original image."""
    
    # Load the image
    img_original = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the original image to grayscale
    img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding with GAUSSIAN_C
    adaptive_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize, C)

    # Apply Otsu's thresholding to the result of adaptive thresholding
    _, otsu_thresh = cv2.threshold(adaptive_thresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply the otsu_thresh mask to the original color image
    img_interseccion = cv2.bitwise_and(img_original, img_original, mask=otsu_thresh)

    area_final = cv2.countNonZero(otsu_thresh)

    return img_interseccion, area_final
