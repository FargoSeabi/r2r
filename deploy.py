#!/usr/bin/env python3
"""
Deployment script for Roots to Realities Django application
This script helps automate the deployment process to Heroku
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_requirements():
    """Check if all required files exist"""
    required_files = ['Procfile', 'requirements.txt', 'runtime.txt', '.env.example']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required deployment files are present")
    return True

def main():
    print("🚀 Roots to Realities Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the Django project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n📝 Please ensure all required files are created before deployment")
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Check if git is initialized
    if not Path('.git').exists():
        print("\n📝 Initializing Git repository...")
        if not run_command("git init", "Initializing Git"):
            sys.exit(1)
    
    # Add and commit files
    if not run_command("git add .", "Adding files to Git"):
        sys.exit(1)
    
    if not run_command('git commit -m "Prepare for deployment"', "Committing changes"):
        print("ℹ️  No changes to commit or already committed")
    
    print("\n🎉 Your application is ready for deployment!")
    print("\nNext steps:")
    print("1. Create a Heroku app: heroku create your-app-name")
    print("2. Set environment variables (see .env.example)")
    print("3. Deploy: git push heroku main")
    print("4. Run migrations: heroku run python manage.py migrate")
    print("5. Create superuser: heroku run python manage.py createsuperuser")
    
    print("\n📖 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main()