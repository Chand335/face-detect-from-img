# Face Detection from Images

A Python application that detects faces in images using OpenCV.

## Features

- Face detection from image URLs
- Batch processing of multiple URLs
- Base64 image upload support
- Visual feedback with rectangles around detected faces
- RESTful API endpoints
- Interactive web interface

## Requirements

- Python 3.x
- OpenCV
- numpy
- Flask
- Requests
- Flask-CORS

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-face-delect-from-image
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to `http://localhost:5001`

## Usage

Run the script with an image file:

```bash
python face_detection.py path/to/image.jpg
```

## API Usage

The application provides two main endpoints:

### 1. Single Image Detection
```bash
POST /api/v1/detect
Content-Type: application/json

{
    "url": "https://example.com/image.jpg"
}
```

### 2. Bulk Image Detection
```bash
POST /api/v1/detect-bulk
Content-Type: application/json

{
    "urls": [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ]
}
```

For detailed API documentation, visit `/api/docs` when the application is running.

## Notes

- The application uses OpenCV's Haar Cascade classifier for face detection
- Best results are achieved with clear, front-facing faces
- Supported image formats: JPG, PNG
- Maximum recommended batch size: 10 images
