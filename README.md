# Car Analysis AI 🚗

Advanced AI-powered image analysis platform for automotive inspection and diagnostics using GPT-4 Vision.

![Car Analysis AI](https://img.shields.io/badge/AI-GPT--4%20Vision-blue) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green) ![React](https://img.shields.io/badge/Frontend-React-cyan)

## 🌟 Features

### 1. White Pixel Detection 🔍
- Upload any image to analyze white pixel concentration
- Accurate pixel counting algorithm
- Detailed percentage metrics and quality assessment
- Useful for image quality control and overexposure detection

### 2. Car Bonnet Analysis 🚗
AI-powered analysis using GPT-4 Vision providing:
- **Automatic Color Identification**: Detects primary car color
- **Condition Assessment**: Evaluates if condition is Good or Bad
- **Wash/Repaint Recommendations**: Professional maintenance advice
- **Issue Detection**: Identifies scratches, dents, rust, paint damage, dirt
- **Part Replacement Suggestions**: Specific repair recommendations
- **Detailed Diagnostic Reports**: Comprehensive action items

### 3. Analysis Dashboard 📊
- View complete analysis history
- Track all previous inspections
- Quick access to detailed reports
- Real-time analysis status

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **MongoDB**: NoSQL database for analysis storage
- **emergentintegrations**: Custom library for LLM integrations
- **GPT-4 Vision (OpenAI)**: Advanced image analysis AI
- **Pillow**: Image processing library

### Frontend
- **React 19**: Modern UI framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icon library
- **Shadcn/UI**: Component library
- **Sonner**: Toast notifications
- **Tailwind CSS**: Utility-first CSS framework

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ with Yarn
- MongoDB running on localhost:27017
- Emergent LLM Key (or OpenAI API key)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd car-analysis-ai
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your credentials
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Configure environment variables
cp .env.example .env
# Edit .env with your backend URL
```

## ⚙️ Configuration

### Backend Environment Variables (`backend/.env`)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=car_analysis_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your-emergent-key-here
```

### Frontend Environment Variables (`frontend/.env`)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🏃 Running the Application

### Development Mode

#### Start Backend
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

#### Start Frontend
```bash
cd frontend
yarn start
```

Access the application at: `http://localhost:3000`

### Production Mode

#### Backend
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

#### Frontend
```bash
cd frontend
yarn build
# Serve the build folder with your preferred web server
```

## 📡 API Documentation

### Base URL
```
http://localhost:8001/api
```

### Endpoints

#### 1. White Pixel Analysis
```http
POST /api/analyze/white-pixels
Content-Type: multipart/form-data

Parameters:
- file: image file (required)

Response:
{
  \"id\": \"uuid\",
  \"analysis_type\": \"white_pixel\",
  \"image_name\": \"image.jpg\",
  \"white_pixel_count\": 5000,
  \"total_pixels\": 10000,
  \"percentage\": 50.0,
  \"analysis_result\": \"High white pixel concentration...\",
  \"timestamp\": \"2025-01-14T10:00:00Z\"
}
```

#### 2. Car Bonnet Analysis
```http
POST /api/analyze/bonnet
Content-Type: multipart/form-data

Parameters:
- file: car bonnet image file (required)

Response:
{
  \"id\": \"uuid\",
  \"analysis_type\": \"bonnet\",
  \"image_name\": \"bonnet.jpg\",
  \"car_color\": \"Red\",
  \"condition\": \"Good\",
  \"wash_or_repaint\": \"Wash\",
  \"issues\": [\"Light dust accumulation\"],
  \"recommendations\": [\"Regular washing recommended\"],
  \"detailed_report\": \"Full diagnostic report...\",
  \"timestamp\": \"2025-01-14T10:00:00Z\"
}
```

#### 3. Get Analysis History
```http
GET /api/analysis/history

Response:
[
  {
    \"id\": \"uuid\",
    \"analysis_type\": \"bonnet\",
    \"image_name\": \"bonnet.jpg\",
    \"timestamp\": \"2025-01-14T10:00:00Z\",
    \"summary\": \"Color: Red | Condition: Good | Wash\"
  }
]
```

#### 4. Get Analysis Detail
```http
GET /api/analysis/{analysis_id}

Response:
{
  // Full analysis object with all details
}
```

## 🎨 User Interface

### Homepage
- Two analysis cards for feature selection
- Modern purple gradient background
- Responsive design
- Clear call-to-action buttons

### Upload Modal
- Drag-and-drop interface
- File browser fallback
- Selected file preview
- Real-time upload progress

### Dashboard
- Grid layout of analysis history
- Quick summary cards
- Click to view detailed reports
- Refresh functionality

### Detail Page
- Comprehensive analysis results
- Visual report sections
- Issue highlighting
- Actionable recommendations

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
yarn test
```

### Manual Testing
1. Upload a pure white image for white pixel detection (should show 100%)
2. Upload a car bonnet image for AI analysis
3. Check dashboard for saved analyses
4. Click on analysis cards to view detailed reports

## 📁 Project Structure

```
car-analysis-ai/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── .env                   # Environment variables
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Global styles
│   │   ├── pages/
│   │   │   ├── HomePage.jsx   # Landing page
│   │   │   ├── Dashboard.jsx  # History dashboard
│   │   │   └── AnalysisDetail.jsx  # Detail view
│   │   └── components/
│   │       └── ui/           # Shadcn UI components
│   ├── package.json          # Node dependencies
│   └── .env                  # Frontend environment
└── README.md                 # This file
```

## 🔑 Key Technologies

### AI Integration
- **emergentintegrations**: Custom library for simplified LLM integration
- **GPT-4 Vision**: Advanced multimodal AI for image understanding
- **Emergent LLM Key**: Universal API key for multiple AI providers

### Image Processing
- **Pillow (PIL)**: Python image processing library
- RGB pixel analysis for white pixel detection
- Base64 encoding for API transmission

### Database
- **MongoDB**: Document-based NoSQL database
- **Motor**: Async MongoDB driver for Python
- Automatic ISO datetime serialization

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 Vision API
- **Emergent Labs** for emergentintegrations library
- **FastAPI** for the excellent Python web framework
- **React** team for the amazing frontend library
- **Shadcn/UI** for beautiful component design


## 🔮 Future Enhancements

- [ ] Support for multiple car angles (hood, doors, wheels)
- [ ] Damage severity scoring system
- [ ] Cost estimation for repairs
- [ ] Export reports as PDF
- [ ] Batch image analysis
- [ ] User authentication and profiles
- [ ] Image comparison (before/after)
- [ ] Mobile app version
- [ ] Real-time camera analysis

## 📸 Screenshots
<img width="1615" height="870" alt="image" src="https://github.com/user-attachments/assets/6b426612-51c5-41e2-bcfa-d51891bb1561" />

### Homepage
Clean, modern interface with two analysis options

### Dashboard
View all previous analyses with quick summaries

### Detail View
Comprehensive reports with visual highlights and recommendations

## Author
Bindu gowda (bindusgowda35@gmail.com)
---
