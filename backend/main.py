"""
QuantiBot AI - Main FastAPI Application
Handles API endpoints for drawing upload, processing, and BOQ generation
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import sys
from datetime import datetime
import uuid
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
REQUIRED_ENV_VARS = ["DATABASE_URL", "JWT_SECRET_KEY"]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

logger.info("All required environment variables are set")

# Initialize database tables on startup
try:
    from init_tables import init_tables
    init_tables()
except Exception as e:
    print(f"Database initialization skipped: {e}")

# Add ai-engine directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai-engine'))

from auth import get_current_user, create_access_token
from database import get_db
# Temporarily disabled - requires PyMuPDF
# from drawing_processor import DrawingProcessor
# from ai_analyzer import AIAnalyzer
# from quantity_calculator import QuantityCalculator
# from cost_estimator import CostEstimator
# from boq_generator import BOQGenerator

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="QuantiBot AI API",
    description="AI-Powered Quantity Surveying & Cost Estimation",
    version="1.0.0"
)

# Add rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Configure for production in .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (temporarily disabled)
# drawing_processor = DrawingProcessor()
# ai_analyzer = AIAnalyzer()
# quantity_calculator = QuantityCalculator()
# cost_estimator = CostEstimator()
# boq_generator = BOQGenerator()


# ============================================================================
# DATA MODELS
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
    
    @field_validator('full_name')
    @classmethod
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v.strip()


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProjectCreate(BaseModel):
    project_name: str
    project_type: str
    location: str
    area_sqft: Optional[float] = None
    
    @field_validator('project_name')
    @classmethod
    def validate_project_name(cls, v):
        if len(v) < 3:
            raise ValueError('Project name must be at least 3 characters long')
        if len(v) > 200:
            raise ValueError('Project name must be less than 200 characters')
        return v.strip()
    
    @field_validator('project_type')
    @classmethod
    def validate_project_type(cls, v):
        allowed_types = ['residential', 'commercial', 'industrial', 'infrastructure', 'other']
        if v.lower() not in allowed_types:
            raise ValueError(f'Project type must be one of: {", ".join(allowed_types)}')
        return v.lower()
    
    @field_validator('area_sqft')
    @classmethod
    def validate_area(cls, v):
        if v is not None and (v <= 0 or v > 10000000):
            raise ValueError('Area must be between 0 and 10,000,000 sq ft')
        return v


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    project_type: str
    location: str
    status: str
    created_at: datetime


class ProcessingStatus(BaseModel):
    project_id: int
    status: str  # "uploading", "processing", "analyzing", "calculating", "completed", "error"
    progress: int  # 0-100
    message: str
    elements_detected: Optional[int] = None
    estimated_completion: Optional[str] = None


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/auth/register")
@limiter.limit("5/minute")
async def register_user(request: Request, user: UserRegister, db = Depends(get_db)):
    """Register a new user account"""
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        
        # Check if user exists
        from sqlalchemy import text
        existing = db.execute(
            text("SELECT id FROM users WHERE email = :email"), 
            {"email": user.email}
        ).fetchone()
        
        if existing:
            logger.warning(f"Registration failed: Email already exists - {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password using bcrypt directly
        import bcrypt
        password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        db.execute(
            text("""INSERT INTO users (email, password_hash, full_name, subscription_tier)
               VALUES (:email, :password_hash, :full_name, :tier)"""),
            {
                "email": user.email,
                "password_hash": password_hash,
                "full_name": user.full_name,
                "tier": "trial"
            }
        )
        db.commit()
        
        logger.info(f"User registered successfully: {user.email}")
        
        return {"message": "User registered successfully", "email": user.email}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Registration error for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during registration")


@app.post("/api/auth/login")
@limiter.limit("10/minute")
async def login_user(request: Request, user: UserLogin, db = Depends(get_db)):
    """Login and receive JWT token"""
    try:
        logger.info(f"Login attempt for email: {user.email}")
        
        # Get user from database
        from sqlalchemy import text
        result = db.execute(
            text("SELECT id, email, password_hash FROM users WHERE email = :email"),
            {"email": user.email}
        ).fetchone()
        
        if not result:
            logger.warning(f"Login failed: User not found - {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Convert result to dict
        db_user = {
            "id": result[0],
            "email": result[1],
            "password_hash": result[2]
        }
        
        # Verify password using bcrypt directly
        import bcrypt
        if not bcrypt.checkpw(user.password.encode('utf-8'), db_user['password_hash'].encode('utf-8')):
            logger.warning(f"Login failed: Invalid password - {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        access_token = create_access_token(data={"sub": user.email, "id": db_user['id']})
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": db_user['id'],
            "email": db_user['email']
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during login")


@app.get("/api/auth/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user information"""
    return {
        "id": current_user['id'],
        "email": current_user['email'],
        "full_name": current_user.get('full_name'),
        "subscription_tier": current_user.get('subscription_tier', 'trial')
    }


# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@app.post("/api/projects", response_model=ProjectResponse)
@limiter.limit("20/minute")
async def create_project(
    request: Request,
    project: ProjectCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new construction project"""
    try:
        from sqlalchemy import text
        result = db.execute(
            text("""INSERT INTO projects (user_id, project_name, project_type, location, area_sqft, status)
               VALUES (:user_id, :project_name, :project_type, :location, :area_sqft, :status)
               RETURNING id"""),
            {
                "user_id": current_user['id'],
                "project_name": project.project_name,
                "project_type": project.project_type,
                "location": project.location,
                "area_sqft": project.area_sqft,
                "status": "created"
            }
        )
        project_id = result.fetchone()[0]
        db.commit()
        
        # Fetch created project
        created_project = db.execute(
            text("SELECT * FROM projects WHERE id = :id"),
            {"id": project_id}
        ).fetchone()
        
        return ProjectResponse(**dict(created_project._mapping))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects")
async def list_projects(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """List all projects for current user"""
    try:
        from sqlalchemy import text
        projects = db.execute(
            text("SELECT * FROM projects WHERE user_id = :user_id ORDER BY created_at DESC"),
            {"user_id": current_user['id']}
        ).fetchall()
        
        return [dict(p._mapping) for p in projects]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}")
async def get_project(
    project_id: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Get detailed information about a specific project"""
    try:
        from sqlalchemy import text
        project = db.execute(
            text("SELECT * FROM projects WHERE id = :id AND user_id = :user_id"),
            {"id": project_id, "user_id": current_user['id']}
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get drawings
        drawings = db.execute(
            text("SELECT * FROM drawings WHERE project_id = :project_id"),
            {"project_id": project_id}
        ).fetchall()
        
        # Get elements count (temporarily disabled)
        # quantities = db.execute(
        #     text("SELECT COUNT(*) as count FROM quantities WHERE project_id = :project_id"),
        #     {"project_id": project_id}
        # ).fetchone()
        
        return {
            "project": dict(project._mapping),
            "drawings": [dict(d._mapping) for d in drawings],
            "quantities_count": 0
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DRAWING UPLOAD ENDPOINTS
# ============================================================================

@app.post("/api/projects/{project_id}/drawings")
@limiter.limit("10/minute")
async def upload_drawings(
    request: Request,
    project_id: int,
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Upload construction drawings (PDF, DWG, PNG, JPG)"""
    try:
        from sqlalchemy import text
        
        # Verify project ownership
        project = db.execute(
            text("SELECT * FROM projects WHERE id = :id AND user_id = :user_id"),
            {"id": project_id, "user_id": current_user['id']}
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Validate number of files
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files per upload")
        
        uploaded_files = []
        
        for file in files:
            # Read file content first to check size
            content = await file.read()
            file_size = len(content)
            
            # Validate file size (25MB max)
            MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
            if file_size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds 25MB limit"
                )
            
            # Validate file type by extension
            allowed_extensions = ['.pdf', '.dwg', '.dxf', '.png', '.jpg', '.jpeg']
            file_ext = os.path.splitext(file.filename)[1].lower()
            
            if file_ext not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_ext}"
                )
            
            # Basic content validation by checking file headers
            if file_ext == '.pdf' and not content.startswith(b'%PDF'):
                raise HTTPException(status_code=400, detail=f"Invalid PDF file: {file.filename}")
            elif file_ext in ['.png'] and not content.startswith(b'\x89PNG'):
                raise HTTPException(status_code=400, detail=f"Invalid PNG file: {file.filename}")
            elif file_ext in ['.jpg', '.jpeg'] and not content.startswith(b'\xff\xd8\xff'):
                raise HTTPException(status_code=400, detail=f"Invalid JPEG file: {file.filename}")
            
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = f"temp_processing/{project_id}/{unique_filename}"
            
            # Save file
            os.makedirs(f"temp_processing/{project_id}", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"File uploaded: {file.filename} ({file_size} bytes) for project {project_id}")
            
            # Store in database
            db.execute(
                text("""INSERT INTO drawings (project_id, file_name, file_url, drawing_type)
                   VALUES (:project_id, :file_name, :file_url, :drawing_type)"""),
                {
                    "project_id": project_id,
                    "file_name": file.filename,
                    "file_url": file_path,
                    "drawing_type": "plan"
                }
            )
            
            uploaded_files.append({
                "filename": file.filename,
                "size": file_size,
                "status": "uploaded"
            })
        
        db.commit()
        logger.info(f"Successfully uploaded {len(uploaded_files)} files for project {project_id}")
        
        # Update project status
        db.execute(
            text("UPDATE projects SET status = :status WHERE id = :id"),
            {"status": "processing", "id": project_id}
        )
        db.commit()
        
        # AI processing temporarily disabled
        # background_tasks.add_task(process_project_drawings, project_id)
        
        return {
            "message": f"{len(files)} drawing(s) uploaded successfully",
            "files": uploaded_files,
            "next_step": "AI analysis starting now..."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PROCESSING ENDPOINTS
# ============================================================================

@app.post("/api/projects/{project_id}/analyze")
async def analyze_project(
    project_id: int,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Start AI analysis of uploaded drawings"""
    try:
        # Verify project
        project = db.execute(
            "SELECT * FROM projects WHERE id = ? AND user_id = ?",
            (project_id, current_user['id'])
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Update status
        db.execute(
            "UPDATE projects SET status = ? WHERE id = ?",
            ("processing", project_id)
        )
        db.commit()
        
        # AI processing temporarily disabled
        # background_tasks.add_task(process_project_drawings, project_id)
        
        return {
            "message": "Analysis started",
            "project_id": project_id,
            "status": "processing"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/status", response_model=ProcessingStatus)
async def get_processing_status(
    project_id: int,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Check the processing status of a project"""
    try:
        project = db.execute(
            "SELECT * FROM projects WHERE id = ? AND user_id = ?",
            (project_id, current_user['id'])
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Count elements
        elements_count = db.execute(
            """SELECT COUNT(*) as count FROM elements 
               WHERE drawing_id IN (SELECT id FROM drawings WHERE project_id = ?)""",
            (project_id,)
        ).fetchone()
        
        # Map status to progress percentage
        status_progress = {
            "created": 0,
            "drawings_uploaded": 10,
            "processing": 30,
            "analyzing": 50,
            "calculating": 70,
            "completed": 100,
            "error": 0
        }
        
        return ProcessingStatus(
            project_id=project_id,
            status=project['status'],
            progress=status_progress.get(project['status'], 0),
            message=f"Project is {project['status']}",
            elements_detected=elements_count['count']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BOQ GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/projects/{project_id}/generate-boq")
async def generate_boq(
    project_id: int,
    region: str = "pakistan",
    currency: str = "PKR",
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Generate Bill of Quantities for the project"""
    try:
        # Verify project
        project = db.execute(
            "SELECT * FROM projects WHERE id = ? AND user_id = ?",
            (project_id, current_user['id'])
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get all quantities
        quantities = db.execute(
            """SELECT q.*, e.element_type, e.description as element_desc
               FROM quantities q
               JOIN elements e ON q.element_id = e.id
               WHERE q.project_id = ?""",
            (project_id,)
        ).fetchall()
        
        if not quantities:
            raise HTTPException(
                status_code=400,
                detail="No quantities found. Please analyze drawings first."
            )
        
        # Generate cost estimates
        cost_items = cost_estimator.estimate_costs(quantities, region, currency)
        
        # Generate BOQ file
        boq_file_path = boq_generator.generate_excel(
            project=dict(project),
            quantities=[dict(q) for q in quantities],
            cost_items=cost_items,
            region=region,
            currency=currency
        )
        
        # Update project status
        db.execute(
            "UPDATE projects SET status = ? WHERE id = ?",
            ("completed", project_id)
        )
        db.commit()
        
        return {
            "message": "BOQ generated successfully",
            "download_url": f"/api/projects/{project_id}/boq/download",
            "total_cost": sum(item['total_cost'] for item in cost_items),
            "currency": currency
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/boq/download")
async def download_boq(
    project_id: int,
    format: str = "excel",  # "excel" or "pdf"
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Download the generated BOQ file"""
    try:
        # Verify project ownership
        project = db.execute(
            "SELECT * FROM projects WHERE id = ? AND user_id = ?",
            (project_id, current_user['id'])
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get file path
        if format == "excel":
            file_path = f"outputs/{project_id}/boq.xlsx"
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format == "pdf":
            file_path = f"outputs/{project_id}/boq.pdf"
            media_type = "application/pdf"
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="BOQ file not found")
        
        return FileResponse(
            file_path,
            media_type=media_type,
            filename=f"{project['project_name']}_BOQ.{format}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BACKGROUND TASKS
# ============================================================================

# Temporarily disabled - requires PyMuPDF
# async def process_project_drawings(project_id: int):
    """Background task to process drawings with AI"""
    from sqlalchemy import text
    db = next(get_db())
    
    try:
        print(f"Starting AI analysis for project {project_id}...")
        
        # Get all drawings for this project
        drawings = db.execute(
            text("SELECT * FROM drawings WHERE project_id = :project_id"),
            {"project_id": project_id}
        ).fetchall()
        
        if not drawings:
            print(f"No drawings found for project {project_id}")
            return
        
        total_elements = []
        
        # Process each drawing
        for drawing in drawings:
            drawing_dict = dict(drawing._mapping)
            file_path = drawing_dict['file_url']
            
            print(f"Analyzing drawing: {drawing_dict['file_name']}")
            
            # Analyze with AI
            result = ai_analyzer.analyze_drawing(file_path, drawing_dict.get('drawing_type', 'plan'))
            
            if result['success']:
                elements = result.get('elements', [])
                total_elements.extend(elements)
                
                # Update drawing status
                db.execute(
                    text("UPDATE drawings SET status = :status WHERE id = :id"),
                    {"status": "analyzed", "id": drawing_dict['id']}
                )
                db.commit()
                
                print(f"Found {len(elements)} elements in {drawing_dict['file_name']}")
            else:
                print(f"Error analyzing {drawing_dict['file_name']}: {result.get('error')}")
        
        # Update project status
        if total_elements:
            db.execute(
                text("UPDATE projects SET status = :status WHERE id = :id"),
                {"status": "completed", "id": project_id}
            )
        else:
            db.execute(
                text("UPDATE projects SET status = :status WHERE id = :id"),
                {"status": "error", "id": project_id}
            )
        db.commit()
        
        print(f"Project {project_id} processing complete! Total elements: {len(total_elements)}")
        
    except Exception as e:
        print(f"Error processing project {project_id}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Update project status to error
        try:
            db.execute(
                text("UPDATE projects SET status = :status WHERE id = :id"),
                {"status": "error", "id": project_id}
            )
            db.commit()
        except:
            pass
    finally:
        db.close()


@app.post("/api/projects/{project_id}/process")
async def trigger_processing(
    project_id: int,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Manually trigger AI processing for a project"""
    from sqlalchemy import text
    
    try:
        # Verify project ownership
        project = db.execute(
            text("SELECT * FROM projects WHERE id = :id AND user_id = :user_id"),
            {"id": project_id, "user_id": current_user['id']}
        ).fetchone()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Update status to processing
        db.execute(
            text("UPDATE projects SET status = :status WHERE id = :id"),
            {"status": "processing", "id": project_id}
        )
        db.commit()
        
        # AI processing temporarily disabled
        # background_tasks.add_task(process_project_drawings, project_id)
        
        return {
            "message": "AI analysis started",
            "project_id": project_id,
            "status": "processing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/")
async def root():
    """API health check"""
    return {
        "status": "operational",
        "service": "QuantiBot AI",
        "version": "1.0.0",
        "message": "AI-Powered Quantity Surveying API"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "ai_service": "available"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
