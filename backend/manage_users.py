#!/usr/bin/env python3
"""
User management script for Jinsyiyuan System
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jinsyiyuan_backend.settings')
django.setup()

from user.models import User
from django.contrib.auth.hashers import make_password

def update_linhui():
    """Update lihui user"""
    try:
        user = User.objects.get(username='linhui')
        user.department = '企业发展部'
        user.position = '员工'
        user.save()
        print(f"Updated user: {user.username}")
        print(f"  Department: {user.department}")
        print(f"  Position: {user.position}")
    except User.DoesNotExist:
        print("User 'linhui' not found")

def create_user(username, password, department, position, email='', nickname=''):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists")
            return
        
        # Create new user
        user = User(
            username=username,
            password=make_password(password),
            department=department,
            position=position,
            email=email,
            nickname=nickname
        )
        user.save()
        print(f"Created user: {user.username}")
        print(f"  Department: {user.department}")
        print(f"  Position: {user.position}")
    except Exception as e:
        print(f"Error creating user {username}: {e}")

def main():
    print("=== User Management Script ===")
    print("\n1. Updating lihui user...")
    update_linhui()
    
    print("\n2. Creating new users...")
    create_user('wangyaling', '123456', '开发部', '主管')
    create_user('mayunfei', '123456', '阿里业务部', '运营主管')
    create_user('lixiang', '123456', '企业发展部', '主管')
    
    print("\n3. Listing all users...")
    users = User.objects.all()
    for user in users:
        print(f"- {user.username}: {user.departme t} - {user.position}")

if __name__ == "__main__":
    main()
