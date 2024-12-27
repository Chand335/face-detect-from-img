# Face Detection Application Features

## Core Features

### Web Interface
- Upload images via file upload
- Detect faces from image URLs
- Real-time face detection preview
- Multiple image processing support
- Tabbed interface for different input methods

### Face Detection
- Detects multiple faces in single image
- Draws bounding boxes around detected faces
- Returns face coordinates and dimensions
- Supports various image formats (JPG, PNG, GIF)
- Base64 image processing support

### API Endpoints

#### 1. `/api/v1/detect`
- Single image processing
- Supports:
  - URL input
  - File upload
  - Base64 encoded images
- Returns:
  - Face count
  - Face coordinates
  - Processed image (optional)

#### 2. `/api/v1/detect-bulk`
- Batch processing multiple images
- Input: Array of image URLs
- Returns:
  - Total face count
  - Individual results per image
  - Processing statistics

#### 3. `/detect`
- Legacy endpoint
- Basic face detection
- Returns processed image with face markers

## Technical Capabilities

### Image Processing
- OpenCV face detection
- Haar Cascade Classifier
- Multiple face detection
- Real-time processing
- Image format conversion

### Input Methods
- File upload (multipart/form-data)
- Image URLs
- Base64 encoded images
- Bulk URL processing

### Output Formats
- JSON response
- Base64 encoded images
- Face coordinates
- Processing statistics

## Security Features
- File type validation
- Error handling
- Size limit validation
- Request timeout handling

## Development Features
- API documentation
- Debug mode
- Error logging
- Static file serving
- Template rendering

## Usage Examples
See `/api/docs` endpoint for detailed API usage examples and integration guides.