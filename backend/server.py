from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import base64
from io import BytesIO
from PIL import Image
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Get API Key
API_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Define Models
class WhitePixelAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_type: str = "white_pixel"
    image_name: str
    white_pixel_count: int
    total_pixels: int
    percentage: float
    analysis_result: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BonnetAnalysis(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    analysis_type: str = "bonnet"
    image_name: str
    car_color: str
    condition: str  # good or bad
    wash_or_repaint: str
    issues: List[str]
    recommendations: List[str]
    detailed_report: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnalysisHistory(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    analysis_type: str
    image_name: str
    timestamp: datetime
    summary: str


def count_white_pixels(image_data: bytes) -> dict:
    """Count white pixels in an image"""
    try:
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')
        
        pixels = list(image.getdata())
        total_pixels = len(pixels)
        
        # Count white pixels (threshold for white: R>240, G>240, B>240)
        white_pixels = sum(1 for r, g, b in pixels if r > 240 and g > 240 and b > 240)
        
        percentage = (white_pixels / total_pixels) * 100
        
        return {
            'white_pixel_count': white_pixels,
            'total_pixels': total_pixels,
            'percentage': round(percentage, 2)
        }
    except Exception as e:
        logger.error(f"Error counting white pixels: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


async def analyze_bonnet_with_gpt4(image_data: bytes, filename: str) -> dict:
    """Analyze car bonnet using GPT-4 Vision"""
    try:
        # Convert image to base64
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Create chat instance
        chat = LlmChat(
            api_key=API_KEY,
            session_id=str(uuid.uuid4()),
            system_message="You are an expert automotive inspector specializing in car condition assessment. Provide detailed, professional analysis."
        ).with_model("openai", "gpt-4o")
        
        # Create analysis prompt
        prompt = """Analyze this car bonnet image and provide:
1. Car Color: Identify the primary color of the car
2. Condition: Assess if the condition is 'Good' or 'Bad'
3. Wash or Repaint: Recommend whether the car needs 'Wash' or 'Repaint'
4. Issues: List any visible issues (scratches, dents, rust, paint damage, dirt accumulation, etc.)
5. Recommendations: Provide specific recommendations for maintenance or repair
6. Detailed Report: A comprehensive diagnostic report with action items

Provide your response in this exact format:
COLOR: [color]
CONDITION: [Good/Bad]
RECOMMENDATION: [Wash/Repaint]
ISSUES: [issue1 | issue2 | issue3]
RECOMMENDATIONS: [rec1 | rec2 | rec3]
DETAILED_REPORT: [detailed analysis]"""
        
        # Create image content
        image_content = ImageContent(image_base64=base64_image)
        
        # Create user message with image
        user_message = UserMessage(
            text=prompt,
            file_contents=[image_content]
        )
        
        # Send message and get response
        response = await chat.send_message(user_message)
        
        # Parse response
        result = parse_gpt4_response(response)
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing bonnet with GPT-4: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")


def parse_gpt4_response(response: str) -> dict:
    """Parse GPT-4 response into structured data"""
    try:
        lines = response.split('\n')
        result = {
            'car_color': 'Unknown',
            'condition': 'Unknown',
            'wash_or_repaint': 'Unknown',
            'issues': [],
            'recommendations': [],
            'detailed_report': response
        }
        
        for line in lines:
            if line.startswith('COLOR:'):
                result['car_color'] = line.replace('COLOR:', '').strip()
            elif line.startswith('CONDITION:'):
                result['condition'] = line.replace('CONDITION:', '').strip()
            elif line.startswith('RECOMMENDATION:'):
                result['wash_or_repaint'] = line.replace('RECOMMENDATION:', '').strip()
            elif line.startswith('ISSUES:'):
                issues_str = line.replace('ISSUES:', '').strip()
                result['issues'] = [i.strip() for i in issues_str.split('|') if i.strip()]
            elif line.startswith('RECOMMENDATIONS:'):
                recs_str = line.replace('RECOMMENDATIONS:', '').strip()
                result['recommendations'] = [r.strip() for r in recs_str.split('|') if r.strip()]
            elif line.startswith('DETAILED_REPORT:'):
                result['detailed_report'] = line.replace('DETAILED_REPORT:', '').strip()
        
        return result
        
    except Exception as e:
        logger.error(f"Error parsing GPT-4 response: {str(e)}")
        return {
            'car_color': 'Unknown',
            'condition': 'Unknown',
            'wash_or_repaint': 'Unknown',
            'issues': ['Error parsing analysis'],
            'recommendations': ['Please try again'],
            'detailed_report': response
        }


# Routes
@api_router.get("/")
async def root():
    return {"message": "Car Analysis API"}


@api_router.post("/analyze/white-pixels")
async def analyze_white_pixels(file: UploadFile = File(...)):
    """Analyze image for white pixels"""
    try:
        # Read image data
        image_data = await file.read()
        
        # Count white pixels
        pixel_data = count_white_pixels(image_data)
        
        # Generate analysis result
        percentage = pixel_data['percentage']
        if percentage > 50:
            analysis_result = f"High white pixel concentration ({percentage}%). Image appears to be predominantly white or overexposed."
        elif percentage > 20:
            analysis_result = f"Moderate white pixel concentration ({percentage}%). Image contains significant white areas."
        elif percentage > 5:
            analysis_result = f"Low white pixel concentration ({percentage}%). Image has some white areas."
        else:
            analysis_result = f"Minimal white pixel concentration ({percentage}%). Image has very few white areas."
        
        # Create analysis record
        analysis = WhitePixelAnalysis(
            image_name=file.filename,
            white_pixel_count=pixel_data['white_pixel_count'],
            total_pixels=pixel_data['total_pixels'],
            percentage=pixel_data['percentage'],
            analysis_result=analysis_result
        )
        
        # Save to database
        doc = analysis.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.analyses.insert_one(doc)
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in white pixel analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/analyze/bonnet")
async def analyze_bonnet(file: UploadFile = File(...)):
    """Analyze car bonnet image"""
    try:
        # Read image data
        image_data = await file.read()
        
        # Analyze with GPT-4 Vision
        gpt4_result = await analyze_bonnet_with_gpt4(image_data, file.filename)
        
        # Create analysis record
        analysis = BonnetAnalysis(
            image_name=file.filename,
            car_color=gpt4_result['car_color'],
            condition=gpt4_result['condition'],
            wash_or_repaint=gpt4_result['wash_or_repaint'],
            issues=gpt4_result['issues'],
            recommendations=gpt4_result['recommendations'],
            detailed_report=gpt4_result['detailed_report']
        )
        
        # Save to database
        doc = analysis.model_dump()
        doc['timestamp'] = doc['timestamp'].isoformat()
        await db.analyses.insert_one(doc)
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error in bonnet analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/analysis/history", response_model=List[AnalysisHistory])
async def get_analysis_history():
    """Get analysis history"""
    try:
        # Fetch all analyses
        analyses = await db.analyses.find({}, {"_id": 0}).sort("timestamp", -1).to_list(100)
        
        # Convert to history format
        history = []
        for analysis in analyses:
            if isinstance(analysis['timestamp'], str):
                analysis['timestamp'] = datetime.fromisoformat(analysis['timestamp'])
            
            if analysis['analysis_type'] == 'white_pixel':
                summary = f"White Pixels: {analysis['percentage']}%"
            else:
                summary = f"Color: {analysis['car_color']} | Condition: {analysis['condition']} | {analysis['wash_or_repaint']}"
            
            history.append(AnalysisHistory(
                id=analysis['id'],
                analysis_type=analysis['analysis_type'],
                image_name=analysis['image_name'],
                timestamp=analysis['timestamp'],
                summary=summary
            ))
        
        return history
        
    except Exception as e:
        logger.error(f"Error fetching analysis history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/analysis/{analysis_id}")
async def get_analysis_detail(analysis_id: str):
    """Get detailed analysis by ID"""
    try:
        analysis = await db.analyses.find_one({"id": analysis_id}, {"_id": 0})
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if isinstance(analysis['timestamp'], str):
            analysis['timestamp'] = datetime.fromisoformat(analysis['timestamp'])
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analysis detail: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()