#!/bin/bash
# Script to create a new user in the Lunaverse Show Brain database

echo "=== Lunaverse Show Brain - User Creation ==="
echo ""
read -p "Enter email address: " email
read -sp "Enter password: " password
echo ""
read -p "Enter role (admin/pm/viewer) [default: admin]: " role
role=${role:-admin}

echo ""
echo "Creating user..."

# Run inside Docker container
docker compose -f infrastructure/docker-compose.yml exec -T api python3 << EOF
import sys
sys.path.append('/app')
from app.db.base import SessionLocal
from app.models.users import User
from app.auth.password_hash import hash_password

db = SessionLocal()
try:
    user = User(
        email='$email',
        password_hash=hash_password('$password'),
        role='$role'
    )
    db.add(user)
    db.commit()
    print(f"✅ User '$email' created successfully with role '$role'!")
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
EOF

echo ""
echo "Done!"

