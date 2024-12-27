import os
from flask import Flask, request, render_template, jsonify, url_for
import cv2
import numpy as np
import requests
import base64
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')

def draw_faces(image, faces):
    image_with_faces = image.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(image_with_faces, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return image_with_faces

def process_image(image, return_image=True):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if return_image:
        image_with_faces = draw_faces(image, faces)
        _, buffer = cv2.imencode('.jpg', image_with_faces)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

    face_list = [{'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)} for (x, y, w, h) in faces]

    result = {
        'face_count': len(faces),
        'faces': face_list,
        'message': f"Detected {len(faces)} face{'s' if len(faces) != 1 else ''} in the image"
    }

    if return_image:
        result['image_with_faces'] = f'data:image/jpeg;base64,{image_base64}'

    return result
   
@app.route('/api/v1/detect', methods=['POST'])
def detect_faces():
    try:
        # Check if request contains JSON
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400

        # Get the data from request
        data = request.get_json()
        
        # Check if either image or url is provided
        if 'image' not in data and 'url' not in data:
            return jsonify({'error': 'Either image data or image URL is required'}), 400

        # Handle URL if provided
        if 'url' in data:
            try:
                response = requests.get(data['url'], timeout=10)
                response.raise_for_status()
                image_data = response.content
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                return jsonify({'error': f'Failed to fetch image from URL: {str(e)}'}), 400
        else:
            # Handle base64 image
            try:
                image_data = base64.b64decode(data['image'].split(',')[1] if ',' in data['image'] else data['image'])
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except Exception as e:
                return jsonify({'error': 'Invalid image encoding'}), 400

        if image is None:
            return jsonify({'error': 'Invalid image data'}), 400

        # Use process_image function
        result = process_image(image, True)
        
        # Add source URL if it was provided
        if 'url' in data:
            result['source_url'] = data['url']

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/detect-bulk', methods=['POST'])
def bulk_detect_faces():
    try:
        # Early validation with simple type checking
        if not isinstance(request.json, dict):
            return jsonify({'error': 'Request must be JSON'}), 400

        urls = request.json.get('urls')
        if not urls:
            return jsonify({'error': 'No URLs provided'}), 400

        # Cleaner URL list processing
        urls = [url.strip() for url in (urls if isinstance(urls, list) else urls.split(','))]
        urls = list(filter(None, urls))  # Remove empty strings
        
        if not urls:
            return jsonify({'error': 'No valid URLs provided'}), 400

        # Use dictionary comprehension for stats tracking
        stats = {
            'results': [],
            'total_faces': 0,
            'processed_count': 0,
            'failed_count': 0
        }


        # Process URLs in batches if needed
        for url in urls:
            try:
                with requests.get(url, timeout=10) as response:
                    response.raise_for_status()
                    image_array = np.frombuffer(response.content, np.uint8)
                    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                    
                    if image is None:
                        raise ValueError('Invalid image format')

                    result = process_image(image, True)
                    result['url'] = url
                    stats['results'].append(result)
                    stats['total_faces'] += result['face_count']
                    stats['processed_count'] += 1

            except Exception as e:
                stats['results'].append({'url': url, 'error': str(e)})
                stats['failed_count'] += 1

        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
