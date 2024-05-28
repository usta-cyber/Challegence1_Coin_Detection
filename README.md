# Challegence1_Coin_Detection
Challenge 1: Coin object detection 
# Challenge 1: Coin Detection

## Overview
This project demonstrates coin detection using different techniques, starting with the Hough Circle method and improving results by training a YOLOv5 model. The coin dataset was converted into the YOLOv5 format using Roboflow. A SQLite database is integrated for storing images and objects, and results such as object unique IDs, bounding boxes, and centroids. A Flask API is written to serve a simple web page to display the results.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Coin Detection Techniques:** Implemented using Hough Circle method and YOLOv5 model.
- **Dataset Conversion:** Converted COCO format dataset to YOLOv5 format using Roboflow.
- **Database Integration:** SQLite database for storing images, objects, and results.
- **Web Application:** Simple web page to display detection results using Flask API.

## Requirements
- Python 3.10

## Installation
Follow these steps to set up the project on your local system:

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/usta-cyber/Challegence1_Coin_Detection.git
    cd Challegence1_Coin_Detection
    ```

2. **Create a Virtual Environment:**
    ```sh
    python -m venv env
    ```

3. **Activate the Virtual Environment:**
    - On Windows:
        ```sh
        .\env\Scripts\Activate
        ```
    - On macOS/Linux:
        ```sh
        source env/bin/activate
        ```

4. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Run the Flask Server:**
    ```sh
    python .\app.py
    ```

2. **Open the Web Page:**
    - Navigate to `http://127.0.0.1:5000` in your web browser.

## Demo

![demo_video-ezgif com-gif-to-mp4-converter](https://github.com/usta-cyber/Challegence1_Coin_Detection/assets/61576602/e29b4b4b-a94e-49ff-86cf-ce689a2e3835)

<img width="682" alt="upload_image" src="https://github.com/usta-cyber/Challegence1_Coin_Detection/assets/61576602/47f3e6ac-48e1-455b-9e43-7698b12a1405">
<img width="452" alt="Detection_image" src="https://github.com/usta-cyber/Challegence1_Coin_Detection/assets/61576602/0e2ef092-407d-4675-862b-94fad615bb6e">
<img width="436" alt="mask_image" src="https://github.com/usta-cyber/Challegence1_Coin_Detection/assets/61576602/7cc759cd-efde-4726-b761-482cdaf7ab91">
<img width="395" alt="Results" src="https://github.com/usta-cyber/Challegence1_Coin_Detection/assets/61576602/53e1f9ba-d9fc-4a3d-a1d5-cdb04b3736f4">

## Results
The project initially used the Hough Circle method for coin detection, but due to high false positives, a YOLOv5 model was trained for better accuracy. The results, including object unique IDs, bounding boxes, and centroids, are stored in an SQLite database and can be viewed via the web interface.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to see.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Note: Make sure to replace the paths `images/example_image.png` and `videos/demo_video.mp4` with the actual paths to your image and video files in the repository.*




