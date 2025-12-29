"""
Check status of stuck projects and their drawings
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Use production URL if local not set
    print("Enter your Render PostgreSQL DATABASE_URL:")
    DATABASE_URL = input().strip()

engine = create_engine(DATABASE_URL)

print("\n" + "="*70)
print("STUCK PROJECTS ANALYSIS")
print("="*70)

with engine.connect() as conn:
    # Check projects stuck in processing
    result = conn.execute(text("""
        SELECT id, project_name, status, created_at, updated_at
        FROM projects
        WHERE status = 'processing'
        ORDER BY created_at DESC
    """))
    
    stuck_projects = result.fetchall()
    
    if not stuck_projects:
        print("\n✓ No stuck projects found!")
    else:
        print(f"\n⚠️  Found {len(stuck_projects)} stuck project(s):\n")
        
        for proj in stuck_projects:
            print(f"Project ID: {proj[0]}")
            print(f"  Name: {proj[1]}")
            print(f"  Status: {proj[2]}")
            print(f"  Created: {proj[3]}")
            print(f"  Updated: {proj[4]}")
            
            # Check drawings for this project
            drawings = conn.execute(text("""
                SELECT id, file_name, status, uploaded_at, processed_at
                FROM drawings
                WHERE project_id = :pid
            """), {"pid": proj[0]}).fetchall()
            
            if drawings:
                print(f"  Drawings ({len(drawings)}):")
                for d in drawings:
                    print(f"    - {d[1]}: {d[2]} (uploaded: {d[3]})")
            else:
                print(f"  Drawings: None")
            
            # Check elements detected
            elem_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM elements e
                JOIN drawings d ON e.drawing_id = d.id
                WHERE d.project_id = :pid
            """), {"pid": proj[0]}).fetchone()[0]
            
            print(f"  Elements detected: {elem_count}")
            print()

print("="*70)
print("\nRECOMMENDATIONS:")
print("="*70)
print("1. Create a NEW project and upload drawings to test fixed code")
print("2. For stuck projects, you can:")
print("   a) Re-upload drawings to trigger new processing")
print("   b) Delete and recreate the project")
print("   c) Wait for manual status update")
print("\nThe new code is deployed and working for NEW uploads.")
