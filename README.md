# Smart Traffic AI Detection System

An intelligent traffic management system that uses AI-powered computer vision to detect safety compliance (helmet for 2-wheelers, seatbelt for 4-wheelers) and controls traffic signals accordingly.

## Features

- **Helmet Detection**: Detects if 2-wheeler riders are wearing helmets
- **Seatbelt Detection**: Detects if 4-wheeler drivers are wearing seatbelts
- **Real-time Processing**: Live video stream processing using YOLOv8
- **Traffic Signal Control**: Green signal only for compliant vehicles
- **Database Logging**: Tracks violations and compliance statistics
- **REST API**: Integration with traffic management systems
- **Web Dashboard**: Monitor detections and statistics

## Project Structure

```
smart-traffic-ai-detection/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── helmet_detector.py
│   │   ├── seatbelt_detector.py
│   │   └── vehicle_classifier.py
│   ├── traffic_controller/
│   │   ├── signal_controller.py
│   │   └── signal_states.py
│   ├── database/
│   │   ├── db_config.py
│   │   ├── models.py
│   │   └── migrations/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   └── utils/
│       ├── video_processor.py
│       └── helpers.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── docker-compose.yml
├── Dockerfile
└── setup.py
```

## Installation

### Prerequisites
- Python 3.8+
- OpenCV
- YOLOv8
- PostgreSQL or SQLite
- Docker (optional)

### Setup

1. Clone the repository
```bash
git clone https://github.com/nandithaakash27-pixel/smart-traffic-ai-detection.git
cd smart-traffic-ai-detection
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

4. Configure database
```bash
# Edit config.py with your database credentials
```

5. Run the application
```bash
python main.py
```

## API Endpoints

- `POST /api/detect` - Process video frame and detect compliance
- `GET /api/signal/status` - Get current traffic signal status
- `POST /api/signal/control` - Control traffic signal
- `GET /api/statistics` - Get violation and compliance statistics
- `GET /api/violations` - List recent violations

## Configuration

Edit `backend/config.py` to configure:
- Video source (webcam, IP camera, video file)
- Detection confidence threshold
- Signal timing
- Database connection

## License

MIT License
