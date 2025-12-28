# QuantiBot AI - Technical Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  Web App (React) | Mobile App | API Integration             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY (FastAPI)                   │
│  Authentication | Rate Limiting | Request Routing            │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   DRAWING PROCESSOR      │  │   QUANTITY CALCULATOR     │
│  - PDF/DWG Parser        │  │  - Dimension Extraction   │
│  - Image Preprocessing   │  │  - Formula Engine         │
│  - Layout Detection      │  │  - Unit Conversion        │
└──────────────────────────┘  └──────────────────────────┘
            │                              │
            ▼                              ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    AI ANALYSIS ENGINE    │  │    COST ESTIMATOR        │
│  - Claude Sonnet 4.5 API │  │  - Unit Rate Database    │
│  - Element Detection     │  │  - Regional Pricing      │
│  - Text Recognition      │  │  - Material Indexing     │
│  - Classification        │  │  - Labor Cost Calc       │
└──────────────────────────┘  └──────────────────────────┘
            │                              │
            └──────────────┬───────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    BOQ GENERATOR                             │
│  Template Engine | Excel Export | PDF Report | Analytics    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                           │
│  PostgreSQL: Projects | Users | Quantities | Cost Rates      │
│  Redis: Cache | Session | Queue                              │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Drawing Processor
**Purpose:** Extract information from construction drawings

**Capabilities:**
- Parse PDF, DWG, DXF, PNG, JPG files
- Detect drawing scale automatically
- Identify title blocks, legends, dimensions
- Extract text annotations
- Separate different drawing sheets (plan, elevation, section)

**Technology:**
- PyMuPDF for PDF parsing
- ezdxf for DWG/DXF files
- OpenCV for image processing
- pytesseract for OCR

**Input:** Construction drawings (any format)
**Output:** Structured drawing data (JSON)

---

### 2. AI Analysis Engine
**Purpose:** Intelligent interpretation of drawings

**Tasks:**
- Identify structural elements (beams, columns, slabs)
- Detect architectural elements (walls, doors, windows)
- Recognize MEP components
- Extract dimensions and specifications
- Classify element types

**AI Models:**
- **Primary:** Claude Sonnet 4.5 (drawing interpretation)
- **Secondary:** Custom computer vision models
- **Text Understanding:** GPT-4o for specification parsing

**Prompt Engineering Strategy:**
```
System: You are a civil engineering expert analyzing construction drawings.
Task: Identify all structural elements and extract their dimensions.
Output: Structured JSON with element type, dimensions, location, quantity.
```

**Input:** Drawing images + extracted text
**Output:** Structured element list (JSON)

---

### 3. Quantity Calculator
**Purpose:** Calculate material quantities from identified elements

**Calculations:**
- **Concrete:** Volume in m³ (length × width × height)
- **Reinforcement:** Weight in kg (area × density × length)
- **Formwork:** Area in m² (perimeter × height)
- **Masonry:** Volume or area (depends on element)
- **Finishing:** Area calculations for flooring, painting, etc.

**Formula Database:**
```python
FORMULAS = {
    "concrete_volume": lambda l, w, h: l * w * h,
    "rebar_weight": lambda dia, length: (dia**2 / 162) * length,
    "formwork_area": lambda l, h: 2 * (l + w) * h,
    "paint_area": lambda l, w, h: 2 * (l + w) * h + l * w,
    # 100+ more formulas
}
```

**Code Compliance:**
- IBC (International Building Code)
- Eurocode
- IS Codes (India)
- BS Codes (UK)
- Regional codes (customizable)

**Input:** Element data (JSON)
**Output:** Quantity takeoff (JSON)

---

### 4. Cost Estimator
**Purpose:** Apply unit rates and calculate total costs

**Cost Database Structure:**
```sql
CREATE TABLE unit_rates (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(100),
    description TEXT,
    unit VARCHAR(20),
    base_rate DECIMAL(10,2),
    currency VARCHAR(3),
    region VARCHAR(50),
    last_updated TIMESTAMP,
    source VARCHAR(100)
);
```

**Rate Sources:**
- RSMeans (US)
- Spon's (UK)
- CPWD (India/Pakistan)
- Local suppliers
- Historical project data

**Pricing Logic:**
```python
total_cost = sum([
    quantity * unit_rate * regional_factor * 
    inflation_factor * complexity_factor
    for each_item in bill_of_quantities
])
```

**Features:**
- Real-time rate updates
- Regional price variations
- Currency conversion
- Bulk discounts
- Contingency calculations

**Input:** Quantities + region + currency
**Output:** Detailed cost estimate

---

### 5. BOQ Generator
**Purpose:** Create professional Bill of Quantities documents

**Output Formats:**
- Excel (XLSX)
- PDF (professional report)
- CSV (for import to other tools)
- JSON (API integration)

**BOQ Structure:**
```
1. Summary Sheet
   - Project info
   - Total cost breakdown
   - Key quantities
   
2. Detailed BOQ
   - Item number
   - Description
   - Unit
   - Quantity
   - Unit rate
   - Total cost
   
3. Supporting Documents
   - Assumptions
   - Exclusions
   - Terms & conditions
```

**Templates:**
- RICS Standard (UK)
- AACE Standard (US)
- Custom templates per client

---

## Data Flow

### Complete Process Flow

```
1. User uploads drawings → S3/Cloud Storage
2. Webhook triggers processing pipeline
3. Drawing Processor extracts images and text
4. AI Engine analyzes each sheet:
   - Identifies elements
   - Extracts dimensions
   - Classifies types
5. Quantity Calculator processes elements:
   - Applies formulas
   - Aggregates quantities
   - Groups by trade
6. Cost Estimator applies rates:
   - Fetches current unit rates
   - Calculates line items
   - Applies factors
7. BOQ Generator creates outputs:
   - Formats data
   - Generates Excel/PDF
   - Sends to user
8. Results stored in database for revisions
```

**Processing Time:**
- Small project (<50 elements): 2-5 minutes
- Medium project (50-200 elements): 5-15 minutes
- Large project (>200 elements): 15-30 minutes

---

## Database Schema

### Core Tables

```sql
-- Users & Authentication
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    subscription_tier VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    project_name VARCHAR(255) NOT NULL,
    project_type VARCHAR(100),
    location VARCHAR(255),
    area_sqft DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Drawings
CREATE TABLE drawings (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    file_name VARCHAR(255),
    file_url TEXT,
    drawing_type VARCHAR(100),
    scale VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Detected Elements
CREATE TABLE elements (
    id SERIAL PRIMARY KEY,
    drawing_id INTEGER REFERENCES drawings(id),
    element_type VARCHAR(100),
    description TEXT,
    dimensions JSONB,
    location JSONB,
    ai_confidence DECIMAL(3,2)
);

-- Quantities
CREATE TABLE quantities (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    element_id INTEGER REFERENCES elements(id),
    item_description TEXT,
    unit VARCHAR(20),
    quantity DECIMAL(12,3),
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- Cost Estimates
CREATE TABLE cost_items (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    quantity_id INTEGER REFERENCES quantities(id),
    unit_rate DECIMAL(10,2),
    total_cost DECIMAL(12,2),
    currency VARCHAR(3)
);
```

---

## API Endpoints

### Authentication
```
POST   /api/auth/register      - Create new account
POST   /api/auth/login         - Login
POST   /api/auth/logout        - Logout
GET    /api/auth/me            - Get current user
```

### Projects
```
POST   /api/projects           - Create new project
GET    /api/projects           - List all projects
GET    /api/projects/:id       - Get project details
PUT    /api/projects/:id       - Update project
DELETE /api/projects/:id       - Delete project
```

### Drawings
```
POST   /api/projects/:id/drawings        - Upload drawings
GET    /api/projects/:id/drawings        - List drawings
DELETE /api/drawings/:id                 - Delete drawing
```

### Processing
```
POST   /api/projects/:id/analyze         - Start AI analysis
GET    /api/projects/:id/status          - Check processing status
GET    /api/projects/:id/elements        - Get detected elements
POST   /api/projects/:id/calculate       - Calculate quantities
```

### BOQ Generation
```
POST   /api/projects/:id/generate-boq    - Generate BOQ
GET    /api/projects/:id/boq             - Download BOQ (Excel/PDF)
GET    /api/projects/:id/cost-summary    - Get cost summary
```

### Cost Database
```
GET    /api/rates                        - Search unit rates
GET    /api/rates/:region                - Get regional rates
POST   /api/rates                        - Add custom rate (admin)
```

---

## Security Architecture

### Authentication
- JWT tokens (access + refresh)
- Session expiry: 24 hours
- Refresh token: 30 days
- Password hashing: bcrypt (12 rounds)

### Authorization
- Role-based access control (RBAC)
- Roles: User, Admin, Super Admin
- API key authentication for integrations

### Data Protection
- Drawings encrypted at rest (AES-256)
- HTTPS only (TLS 1.3)
- Sensitive data encrypted in database
- Regular backups (daily)

### API Security
- Rate limiting: 100 requests/minute per user
- Input validation and sanitization
- CORS policies
- SQL injection prevention (parameterized queries)

---

## Scalability Strategy

### Horizontal Scaling
- Containerized microservices (Docker)
- Load balancer (Nginx/AWS ELB)
- Multiple API instances
- Background job workers (Celery)

### Database Optimization
- Read replicas for queries
- Connection pooling
- Query optimization and indexing
- Partitioning large tables

### Caching Strategy
```
Redis Cache:
- User sessions (1 hour TTL)
- Unit rates (24 hour TTL)
- Processing status (real-time)
- Common queries (30 min TTL)
```

### Performance Targets
- API response: <200ms (95th percentile)
- Drawing upload: <5 seconds
- Analysis completion: <30 minutes
- Concurrent users: 1000+

---

## Deployment Architecture

### Development Environment
```
Local Machine:
- Docker Compose
- PostgreSQL (local)
- Redis (local)
- Hot reload enabled
```

### Staging Environment
```
AWS/GCP:
- 1x API server (t3.medium)
- 1x Worker instance (t3.medium)
- RDS PostgreSQL (db.t3.small)
- ElastiCache Redis
- S3 for file storage
```

### Production Environment
```
AWS/GCP:
- 3x API servers (t3.large) + Auto-scaling
- 5x Worker instances (c5.xlarge)
- RDS PostgreSQL (db.r5.large) + Read replica
- ElastiCache Redis (cache.r5.large)
- S3 + CloudFront CDN
- Route 53 DNS
- AWS WAF (firewall)
```

---

## Monitoring & Logging

### Application Monitoring
- **APM:** New Relic or DataDog
- **Uptime:** Pingdom
- **Error Tracking:** Sentry
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)

### Business Metrics
- Projects processed per day
- Average processing time
- Accuracy rate (human verification)
- Customer satisfaction score
- Revenue per customer

### Alerts
- API downtime
- Processing failures
- High error rates
- Database performance issues
- Cost anomalies

---

## AI/ML Pipeline

### Model Training (Future Enhancement)
```python
# Custom element detection model
Training Data:
- 10,000+ annotated drawings
- Multiple building types
- Various drawing styles

Model Architecture:
- YOLOv8 for object detection
- ResNet50 for classification
- Custom CNN for dimension extraction

Training Process:
- Data augmentation
- Transfer learning
- Continuous learning from user corrections
```

### Quality Assurance
- Human-in-the-loop verification for first 100 projects
- Confidence scoring for AI predictions
- Manual override capability
- A/B testing for prompt improvements

---

## Cost Structure (Monthly)

### Infrastructure Costs
```
AWS Costs:
- EC2 instances: $300-500
- RDS: $150-250
- S3 storage: $50-100
- Data transfer: $100-200
Total: ~$600-1050/month
```

### AI API Costs
```
Claude API:
- $3-20 per drawing analysis
- Average 100 projects/month
- Total: $300-2000/month (scales with usage)
```

### Total Operating Cost: $900-3,050/month
**At 30 clients × $2,997/month = $89,910 revenue**
**Net profit: $86,860/month (96% margin)**

---

*This architecture supports scaling from 0 to 10,000+ monthly projects.*
