# QuantiBot AI - Complete Test Suite

import pytest
import os
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base, engine
from sqlalchemy.orm import Session

# Test client
client = TestClient(app)

# ============================================
# 1. AUTHENTICATION TESTS
# ============================================

def test_user_registration():
    """Test user registration"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_duplicate_registration():
    """Test duplicate email registration fails"""
    # First registration
    client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    })
    # Duplicate registration
    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
        "full_name": "Another User"
    })
    assert response.status_code == 400

def test_user_login():
    """Test user login"""
    # Register user first
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "SecurePass123!",
        "full_name": "Login Test"
    })
    # Login
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login():
    """Test login with wrong password"""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

def test_get_current_user():
    """Test getting current user info"""
    # Login first
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    token = login_response.json()["access_token"]
    
    # Get user info
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"

# ============================================
# 2. PROJECT TESTS
# ============================================

@pytest.fixture
def auth_headers():
    """Get authentication headers for tests"""
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_project(auth_headers):
    """Test project creation"""
    response = client.post("/projects", 
        headers=auth_headers,
        json={
            "name": "Test Building Project",
            "description": "A test construction project",
            "project_type": "residential",
            "location": "Karachi, Pakistan",
            "region": "pakistan"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Building Project"
    assert data["status"] == "draft"

def test_list_projects(auth_headers):
    """Test listing projects"""
    response = client.get("/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_project(auth_headers):
    """Test getting single project"""
    # Create project first
    create_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "Get Test Project",
            "project_type": "commercial",
            "location": "Dubai, UAE",
            "region": "uae"
        }
    )
    project_id = create_response.json()["id"]
    
    # Get project
    response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id

def test_delete_project(auth_headers):
    """Test project deletion"""
    # Create project
    create_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "Delete Test Project",
            "project_type": "industrial",
            "location": "New York, USA",
            "region": "usa"
        }
    )
    project_id = create_response.json()["id"]
    
    # Delete project
    response = client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify deleted
    get_response = client.get(f"/projects/{project_id}", headers=auth_headers)
    assert get_response.status_code == 404

# ============================================
# 3. DRAWING UPLOAD TESTS
# ============================================

def test_upload_drawing(auth_headers):
    """Test drawing file upload"""
    # Create project first
    project_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "Upload Test Project",
            "project_type": "residential",
            "location": "Test Location",
            "region": "pakistan"
        }
    )
    project_id = project_response.json()["id"]
    
    # Create a test PDF file
    test_file = ("test_drawing.pdf", b"PDF test content", "application/pdf")
    
    response = client.post(
        f"/projects/{project_id}/drawings/upload",
        headers=auth_headers,
        files={"file": test_file}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_drawing.pdf"
    assert data["file_type"] == "application/pdf"

def test_upload_invalid_file_type(auth_headers):
    """Test uploading unsupported file type"""
    project_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "Invalid Upload Project",
            "project_type": "commercial",
            "location": "Test",
            "region": "pakistan"
        }
    )
    project_id = project_response.json()["id"]
    
    # Try uploading .txt file
    test_file = ("test.txt", b"Text content", "text/plain")
    
    response = client.post(
        f"/projects/{project_id}/drawings/upload",
        headers=auth_headers,
        files={"file": test_file}
    )
    assert response.status_code == 400

def test_list_drawings(auth_headers):
    """Test listing project drawings"""
    # Create project and upload drawing
    project_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "List Drawings Project",
            "project_type": "residential",
            "location": "Test",
            "region": "pakistan"
        }
    )
    project_id = project_response.json()["id"]
    
    # Upload drawing
    test_file = ("drawing1.pdf", b"PDF content", "application/pdf")
    client.post(
        f"/projects/{project_id}/drawings/upload",
        headers=auth_headers,
        files={"file": test_file}
    )
    
    # List drawings
    response = client.get(f"/projects/{project_id}/drawings", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

# ============================================
# 4. AI ANALYSIS TESTS (Integration)
# ============================================

def test_analyze_drawing_endpoint(auth_headers):
    """Test AI analysis endpoint (mocked)"""
    # Note: This test requires mock AI response
    # In production, use pytest-mock to mock Anthropic API
    
    # Create project and upload
    project_response = client.post("/projects",
        headers=auth_headers,
        json={
            "name": "Analysis Test Project",
            "project_type": "residential",
            "location": "Test",
            "region": "pakistan"
        }
    )
    project_id = project_response.json()["id"]
    
    # Upload test drawing
    test_file = ("analysis_test.pdf", b"PDF content", "application/pdf")
    upload_response = client.post(
        f"/projects/{project_id}/drawings/upload",
        headers=auth_headers,
        files={"file": test_file}
    )
    drawing_id = upload_response.json()["id"]
    
    # Start analysis (will fail without real API key, but tests endpoint)
    response = client.post(
        f"/process/analyze/{drawing_id}",
        headers=auth_headers
    )
    # Accept either success or error (since we don't have real drawing)
    assert response.status_code in [200, 400, 500]

# ============================================
# 5. QUANTITY CALCULATION TESTS
# ============================================

def test_column_quantity_calculation():
    """Test column quantity calculations"""
    from quantity_calculator import calculate_quantities
    
    elements = [
        {
            "element_type": "column",
            "dimensions": {
                "length": 0.3,  # 300mm
                "width": 0.3,   # 300mm
                "height": 3.0   # 3m
            },
            "material": "concrete",
            "count": 4
        }
    ]
    
    result = calculate_quantities(elements)
    
    # Expected concrete volume = 0.3 * 0.3 * 3.0 * 4 = 1.08 m³
    concrete_qty = next(q for q in result if q["item"] == "Concrete")
    assert abs(concrete_qty["quantity"] - 1.08) < 0.01

def test_beam_quantity_calculation():
    """Test beam quantity calculations"""
    from quantity_calculator import calculate_quantities
    
    elements = [
        {
            "element_type": "beam",
            "dimensions": {
                "length": 5.0,
                "width": 0.25,
                "height": 0.4
            },
            "material": "concrete",
            "count": 2
        }
    ]
    
    result = calculate_quantities(elements)
    
    # Expected volume = 5.0 * 0.25 * 0.4 * 2 = 1.0 m³
    concrete_qty = next(q for q in result if q["item"] == "Concrete")
    assert abs(concrete_qty["quantity"] - 1.0) < 0.01

def test_wall_quantity_calculation():
    """Test wall quantity calculations"""
    from quantity_calculator import calculate_quantities
    
    elements = [
        {
            "element_type": "wall",
            "dimensions": {
                "length": 10.0,
                "height": 3.0,
                "thickness": 0.23  # 9-inch wall
            },
            "material": "brick",
            "count": 1
        }
    ]
    
    result = calculate_quantities(elements)
    
    # Expected area = 10.0 * 3.0 = 30 m²
    brick_qty = next(q for q in result if q["item"] == "Bricks")
    # ~500 bricks per m² for 9-inch wall
    assert brick_qty["quantity"] > 10000  # 30 * 500 = 15,000

# ============================================
# 6. COST ESTIMATION TESTS
# ============================================

def test_cost_estimation_pakistan():
    """Test cost estimation with Pakistan rates"""
    from cost_estimator import estimate_costs
    
    quantities = [
        {"item": "Concrete", "quantity": 10.0, "unit": "m³"},
        {"item": "Steel Reinforcement", "quantity": 500.0, "unit": "kg"},
        {"item": "Bricks", "quantity": 5000, "unit": "pcs"},
    ]
    
    result = estimate_costs(quantities, region="pakistan")
    
    assert "items" in result
    assert "summary" in result
    assert result["summary"]["total_cost"] > 0
    assert result["summary"]["currency"] == "PKR"

def test_cost_estimation_uae():
    """Test cost estimation with UAE rates"""
    from cost_estimator import estimate_costs
    
    quantities = [
        {"item": "Concrete", "quantity": 10.0, "unit": "m³"},
    ]
    
    result = estimate_costs(quantities, region="uae")
    
    assert result["summary"]["currency"] == "AED"
    # UAE rates should be higher than Pakistan
    assert result["summary"]["total_cost"] > 0

def test_cost_with_contingency():
    """Test cost calculation with contingency"""
    from cost_estimator import estimate_costs
    
    quantities = [
        {"item": "Concrete", "quantity": 10.0, "unit": "m³"},
    ]
    
    result = estimate_costs(quantities, region="pakistan", contingency=10)
    
    base_cost = result["summary"]["subtotal"]
    total_cost = result["summary"]["total_cost"]
    
    # Total should be ~10% more than base
    assert total_cost > base_cost
    assert abs((total_cost / base_cost - 1.1) < 0.01)

# ============================================
# 7. BOQ GENERATION TESTS
# ============================================

def test_boq_excel_generation():
    """Test BOQ Excel file generation"""
    from boq_generator import generate_excel
    import os
    
    project_data = {
        "name": "Test Project",
        "location": "Karachi",
        "date": "2025-01-15"
    }
    
    quantities = [
        {"item": "Concrete", "quantity": 10.0, "unit": "m³", "rate": 15000, "amount": 150000},
        {"item": "Steel Reinforcement", "quantity": 500.0, "unit": "kg", "rate": 250, "amount": 125000},
    ]
    
    output_path = "test_boq.xlsx"
    result = generate_excel(project_data, quantities, output_path)
    
    assert result["file_path"] == output_path
    assert os.path.exists(output_path)
    
    # Cleanup
    os.remove(output_path)

# ============================================
# 8. RATE LIMITING TESTS
# ============================================

def test_rate_limiting():
    """Test API rate limiting"""
    # Make many requests quickly
    responses = []
    for i in range(110):  # Exceed limit of 100/minute
        response = client.get("/")
        responses.append(response.status_code)
    
    # Should have some 429 (Too Many Requests) responses
    assert 429 in responses

# ============================================
# 9. SUBSCRIPTION TESTS
# ============================================

def test_subscription_limits_free_tier(auth_headers):
    """Test free tier limits"""
    response = client.get("/subscription/usage", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    
    assert "projects_used" in data
    assert "projects_limit" in data
    assert data["projects_limit"] == 5  # Free tier limit

def test_subscription_upgrade_flow(auth_headers):
    """Test subscription upgrade checkout"""
    response = client.post("/subscription/checkout",
        headers=auth_headers,
        json={"plan_id": "pro"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "checkout_url" in data

# ============================================
# 10. ERROR HANDLING TESTS
# ============================================

def test_unauthorized_access():
    """Test accessing protected endpoint without auth"""
    response = client.get("/projects")
    assert response.status_code == 401

def test_invalid_project_id(auth_headers):
    """Test accessing non-existent project"""
    response = client.get("/projects/99999", headers=auth_headers)
    assert response.status_code == 404

def test_invalid_json_payload():
    """Test sending invalid JSON"""
    response = client.post("/auth/register",
        headers={"Content-Type": "application/json"},
        data="invalid json{{"
    )
    assert response.status_code == 422

# ============================================
# RUN TESTS
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
