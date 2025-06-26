"""
Database setup script to create the personnel table with initial schema.
This script can be run independently to set up the database.
"""

from app import app, db
from models import Personnel
import os

def setup_database():
    """Create all database tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if we can connect and query
        try:
            count = Personnel.query.count()
            print(f"📊 Current personnel count: {count}")
            return True
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False

if __name__ == '__main__':
    # Check for database URL
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        # Check for Railway PostgreSQL environment variables
        pg_host = os.environ.get("PGHOST")
        pg_user = os.environ.get("PGUSER")
        pg_password = os.environ.get("PGPASSWORD")
        pg_database = os.environ.get("PGDATABASE")
        
        if not all([pg_host, pg_user, pg_password, pg_database]):
            print("❌ DATABASE_URL or PostgreSQL environment variables are required")
            print("Please set your database connection in the environment variables")
            exit(1)
    
    success = setup_database()
    if success:
        print("🎉 Database setup completed successfully!")
    else:
        print("💥 Database setup failed!")
        exit(1)
