#!/usr/bin/env python3
"""
Standalone script to create a user in the database.
Run this inside the Docker container or with proper database connection.
"""
import sys
import os

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.db.base import SessionLocal
from app.models.users import User
from app.auth.password_hash import hash_password

def create_user():
    print("=== Lunaverse Show Brain - User Creation ===")
    print()
    
    email = input("Enter email address: ").strip()
    if not email:
        print("Error: Email is required")
        return
    
    password = input("Enter password: ").strip()
    if not password:
        print("Error: Password is required")
        return
    
    role = input("Enter role (admin/pm/viewer) [default: admin]: ").strip() or "admin"
    
    if role not in ['admin', 'pm', 'viewer']:
        print(f"Error: Invalid role '{role}'. Must be admin, pm, or viewer")
        return
    
    db = SessionLocal()
    try:
        # Check if user already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"Error: User with email '{email}' already exists")
            return
        
        user = User(
            email=email,
            password_hash=hash_password(password),
            role=role
        )
        db.add(user)
        db.commit()
        print(f"✅ User '{email}' created successfully with role '{role}'!")
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_user()

