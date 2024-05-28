# version2
# import cv2
# import numpy as np

# def detect_circular_objects(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (9, 9), 2)
#     circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=100)

#     mask = np.zeros_like(gray)
#     circles_data = []

#     if circles is not None:
#         circles = np.round(circles[0, :]).astype("int")
#         for (x, y, r) in circles:
#             cv2.circle(mask, (x, y), r, 255, -1)
#             circles_data.append({'id': len(circles_data), 'bounding_box': (x-r, y-r, x+r, y+r), 'centroid': (x, y), 'radius': r})
#             cv2.rectangle(image, (x-r, y-r), (x+r, y+r), (0, 255, 0), 2)

#     return image, mask, circles_data


##############Version3
import cv2
import numpy as np

def convert_numpy_to_native(data):
    if isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, dict):
        return {k: convert_numpy_to_native(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_native(i) for i in data]
    else:
        return data

def detect_circular_objects(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=30, minRadius=10, maxRadius=100)

    mask = np.zeros_like(gray)
    circles_data = []

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(mask, (x, y), r, 255, -1)
            circles_data.append({
                'id': len(circles_data),
                'bounding_box': (x-r, y-r, x+r, y+r),
                'centroid': (x, y),
                'radius': r
            })
            cv2.rectangle(image, (x-r, y-r), (x+r, y+r), (0, 255, 0), 2)

    # Convert numpy data types to native Python data types
    circles_data = convert_numpy_to_native(circles_data)

    return image, mask, circles_data


