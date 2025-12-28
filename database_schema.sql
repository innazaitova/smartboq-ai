-- QuantiBot AI Database Schema
-- PostgreSQL Database Schema for Quantity Surveying Application

-- ============================================================================
-- USERS & AUTHENTICATION
-- ============================================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_name VARCHAR(255),
    phone VARCHAR(50),
    country VARCHAR(100),
    subscription_tier VARCHAR(50) DEFAULT 'trial',  -- trial, starter, professional, enterprise
    subscription_status VARCHAR(50) DEFAULT 'active', -- active, suspended, cancelled
    subscription_expires_at TIMESTAMP,
    credits_remaining INTEGER DEFAULT 5,  -- For trial users
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier, subscription_status);


-- ============================================================================
-- PROJECTS
-- ============================================================================

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_name VARCHAR(255) NOT NULL,
    project_type VARCHAR(100),  -- residential, commercial, industrial, etc.
    location VARCHAR(255),
    area_sqft DECIMAL(12,2),
    building_code VARCHAR(50) DEFAULT 'IBC',  -- IBC, Eurocode, IS, BS, etc.
    status VARCHAR(50) DEFAULT 'created',  -- created, drawings_uploaded, processing, analyzing, calculating, completed, error
    currency VARCHAR(3) DEFAULT 'PKR',
    total_cost DECIMAL(15,2),
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created ON projects(created_at DESC);


-- ============================================================================
-- DRAWINGS
-- ============================================================================

CREATE TABLE drawings (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    file_size_bytes BIGINT,
    file_type VARCHAR(50),  -- pdf, dwg, dxf, png, jpg
    drawing_type VARCHAR(100) DEFAULT 'plan',  -- plan, elevation, section, detail
    scale VARCHAR(50),  -- 1:100, 1:50, etc.
    sheet_number VARCHAR(50),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'pending'  -- pending, processing, completed, error
);

CREATE INDEX idx_drawings_project ON drawings(project_id);
CREATE INDEX idx_drawings_status ON drawings(processing_status);


-- ============================================================================
-- DETECTED ELEMENTS
-- ============================================================================

CREATE TABLE elements (
    id SERIAL PRIMARY KEY,
    drawing_id INTEGER REFERENCES drawings(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    element_type VARCHAR(100) NOT NULL,  -- column, beam, slab, wall, door, window, etc.
    description TEXT,
    dimensions JSONB,  -- {length: 6.0, width: 0.23, height: 0.45, unit: "meters"}
    location JSONB,  -- {grid: "A-1", floor: "Ground", coordinates: {x: 100, y: 200}}
    material VARCHAR(255),  -- Reinforced Concrete, Brick Masonry, etc.
    quantity INTEGER DEFAULT 1,
    ai_confidence DECIMAL(3,2),  -- 0.00 to 1.00
    ai_raw_response TEXT,  -- Store full AI response
    verified BOOLEAN DEFAULT FALSE,  -- Human verification flag
    verified_by INTEGER REFERENCES users(id),
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_elements_drawing ON elements(drawing_id);
CREATE INDEX idx_elements_project ON elements(project_id);
CREATE INDEX idx_elements_type ON elements(element_type);
CREATE INDEX idx_elements_verified ON elements(verified);


-- ============================================================================
-- QUANTITIES
-- ============================================================================

CREATE TABLE quantities (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    element_id INTEGER REFERENCES elements(id) ON DELETE CASCADE,
    item_description TEXT NOT NULL,
    material VARCHAR(255) NOT NULL,
    unit VARCHAR(20) NOT NULL,  -- m³, m², kg, nos, LS, etc.
    quantity DECIMAL(15,3) NOT NULL,
    formula VARCHAR(500),  -- The formula used for calculation
    element_reference VARCHAR(255),  -- Reference to drawing/grid location
    notes TEXT,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quantities_project ON quantities(project_id);
CREATE INDEX idx_quantities_element ON quantities(element_id);
CREATE INDEX idx_quantities_material ON quantities(material);


-- ============================================================================
-- COST ITEMS
-- ============================================================================

CREATE TABLE cost_items (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    quantity_id INTEGER REFERENCES quantities(id) ON DELETE CASCADE,
    item_description TEXT NOT NULL,
    material VARCHAR(255),
    unit VARCHAR(20),
    quantity DECIMAL(15,3),
    base_unit_rate DECIMAL(12,2),  -- Base rate before factors
    final_unit_rate DECIMAL(12,2),  -- After applying all factors
    total_cost DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'PKR',
    regional_factor DECIMAL(5,3) DEFAULT 1.000,
    project_type_factor DECIMAL(5,3) DEFAULT 1.000,
    inflation_factor DECIMAL(5,3) DEFAULT 1.000,
    rate_source VARCHAR(255),  -- RSMeans, CPWD, Market Survey, etc.
    element_reference VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cost_items_project ON cost_items(project_id);
CREATE INDEX idx_cost_items_quantity ON cost_items(quantity_id);


-- ============================================================================
-- UNIT RATES DATABASE
-- ============================================================================

CREATE TABLE unit_rates (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(100) NOT NULL,
    description TEXT,
    unit VARCHAR(20) NOT NULL,
    base_rate DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    region VARCHAR(50) NOT NULL,  -- pakistan, uae, usa, uk, india, saudi_arabia
    sub_region VARCHAR(50),  -- karachi, dubai, new_york, london, etc.
    source VARCHAR(100),  -- RSMeans, Spon's, CPWD, Market Survey
    effective_date DATE,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_unit_rates_material ON unit_rates(material_type);
CREATE INDEX idx_unit_rates_region ON unit_rates(region, sub_region);
CREATE INDEX idx_unit_rates_active ON unit_rates(is_active);


-- ============================================================================
-- BOQ OUTPUTS
-- ============================================================================

CREATE TABLE boq_outputs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    file_format VARCHAR(10),  -- xlsx, pdf, csv
    file_url TEXT,
    file_size_bytes BIGINT,
    includes_contingency BOOLEAN DEFAULT FALSE,
    contingency_percent DECIMAL(5,2),
    includes_overhead BOOLEAN DEFAULT FALSE,
    overhead_percent DECIMAL(5,2),
    includes_profit BOOLEAN DEFAULT FALSE,
    profit_percent DECIMAL(5,2),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    downloaded_at TIMESTAMP
);

CREATE INDEX idx_boq_outputs_project ON boq_outputs(project_id);


-- ============================================================================
-- PROCESSING LOGS
-- ============================================================================

CREATE TABLE processing_logs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    drawing_id INTEGER REFERENCES drawings(id) ON DELETE CASCADE,
    stage VARCHAR(100),  -- upload, parsing, ai_analysis, quantity_calc, cost_estimate, boq_generation
    status VARCHAR(50),  -- started, in_progress, completed, error
    message TEXT,
    error_details TEXT,
    processing_time_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_processing_logs_project ON processing_logs(project_id);
CREATE INDEX idx_processing_logs_status ON processing_logs(status);


-- ============================================================================
-- API USAGE TRACKING
-- ============================================================================

CREATE TABLE api_usage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    api_provider VARCHAR(50),  -- anthropic, openai, google_vision, etc.
    api_endpoint VARCHAR(100),
    tokens_used INTEGER,
    cost_usd DECIMAL(10,4),
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_api_usage_user ON api_usage(user_id);
CREATE INDEX idx_api_usage_date ON api_usage(created_at DESC);


-- ============================================================================
-- SUBSCRIPTIONS & BILLING
-- ============================================================================

CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'PKR',
    status VARCHAR(50) DEFAULT 'pending',  -- pending, paid, overdue, cancelled
    billing_period_start DATE,
    billing_period_end DATE,
    payment_method VARCHAR(50),  -- stripe, paypal, bank_transfer, etc.
    payment_reference VARCHAR(255),
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invoices_user ON invoices(user_id);
CREATE INDEX idx_invoices_status ON invoices(status);


-- ============================================================================
-- AUDIT LOG
-- ============================================================================

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,  -- login, create_project, upload_drawing, generate_boq, etc.
    entity_type VARCHAR(50),  -- user, project, drawing, etc.
    entity_id INTEGER,
    changes JSONB,  -- Store what changed
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user ON audit_log(user_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);
CREATE INDEX idx_audit_log_date ON audit_log(created_at DESC);


-- ============================================================================
-- SAMPLE DATA - UNIT RATES (PAKISTAN)
-- ============================================================================

INSERT INTO unit_rates (material_type, description, unit, base_rate, currency, region, source, effective_date, is_active) VALUES
('Concrete', 'M25 Grade Concrete', 'm³', 15000, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Reinforcement Steel', 'Grade 60 Deformed Bars', 'kg', 280, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Formwork', 'Plywood Formwork', 'm²', 450, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Bricks', 'Standard Clay Bricks', 'nos', 18, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Mortar', 'Cement Sand Mortar 1:4', 'm³', 8000, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Door panel', 'Solid Wood Door', 'm²', 12000, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Window frame & glass', 'Aluminum Frame with Glass', 'm²', 8000, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Paint', 'Emulsion Paint', 'm²', 120, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Plaster', 'Cement Plaster', 'm²', 180, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE),
('Tiles', 'Ceramic Floor Tiles', 'm²', 1200, 'PKR', 'pakistan', 'Market Survey 2025', '2025-01-01', TRUE);


-- ============================================================================
-- VIEWS
-- ============================================================================

-- Project Summary View
CREATE VIEW v_project_summary AS
SELECT 
    p.id,
    p.project_name,
    p.project_type,
    p.status,
    u.email as owner_email,
    u.company_name,
    COUNT(DISTINCT d.id) as total_drawings,
    COUNT(DISTINCT e.id) as total_elements,
    COUNT(DISTINCT q.id) as total_quantities,
    p.total_cost,
    p.currency,
    p.created_at,
    p.processing_completed_at
FROM projects p
LEFT JOIN users u ON p.user_id = u.id
LEFT JOIN drawings d ON p.id = d.project_id
LEFT JOIN elements e ON p.id = e.project_id
LEFT JOIN quantities q ON p.id = q.project_id
GROUP BY p.id, u.email, u.company_name;


-- User Statistics View
CREATE VIEW v_user_statistics AS
SELECT 
    u.id,
    u.email,
    u.company_name,
    u.subscription_tier,
    COUNT(DISTINCT p.id) as total_projects,
    COUNT(DISTINCT d.id) as total_drawings,
    SUM(p.total_cost) as total_project_value,
    u.created_at as member_since
FROM users u
LEFT JOIN projects p ON u.id = p.user_id
LEFT JOIN drawings d ON p.id = d.project_id
GROUP BY u.id;


-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update project status
CREATE OR REPLACE FUNCTION update_project_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE projects 
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.project_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update project timestamps
CREATE TRIGGER trg_update_project_status
AFTER INSERT OR UPDATE ON drawings
FOR EACH ROW
EXECUTE FUNCTION update_project_status();


-- ============================================================================
-- SEED DATA FOR TESTING
-- ============================================================================

-- Create a test user
INSERT INTO users (email, password_hash, company_name, subscription_tier, credits_remaining)
VALUES ('demo@quantibot.ai', '$2b$12$test_hash_here', 'Demo Construction Ltd', 'professional', 999);


-- ============================================================================
-- DATABASE MAINTENANCE
-- ============================================================================

-- Cleanup old processing logs (keep last 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_logs()
RETURNS void AS $$
BEGIN
    DELETE FROM processing_logs 
    WHERE created_at < CURRENT_DATE - INTERVAL '30 days';
    
    DELETE FROM audit_log 
    WHERE created_at < CURRENT_DATE - INTERVAL '90 days';
END;
$$ LANGUAGE plpgsql;

-- Schedule this to run daily (use pg_cron or external scheduler)
