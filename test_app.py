#!/usr/bin/env python3
"""
Simple test script to validate ClinicCare Flask app structure.
Run this to check if all imports and basic app setup work correctly.
"""

import os
import sys

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        from app import create_app, db
        print("✓ App factory import successful")
        
        from app.models import User, Patient, Visit
        print("✓ Models import successful")
        
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.patients import patients_bp
        from app.routes.analytics import analytics_bp
        from app.routes.admin import admin_bp
        print("✓ All blueprints import successful")
        
        from app.forms import LoginForm, RegistrationForm, PatientForm, VisitForm
        print("✓ Forms import successful")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    return True

def test_app_creation():
    """Test Flask app creation"""
    print("\nTesting app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("✓ Flask app created successfully")
        
        # Check if blueprints are registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        expected_blueprints = ['auth', 'main', 'patients', 'analytics', 'admin']
        
        for bp_name in expected_blueprints:
            if bp_name in blueprint_names:
                print(f"✓ Blueprint '{bp_name}' registered")
            else:
                print(f"✗ Blueprint '{bp_name}' not found")
                return False
                
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False
    
    return True

def test_routes():
    """Test basic route registration"""
    print("\nTesting routes...")
    
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test login page (should be accessible without auth)
            response = client.get('/login')
            if response.status_code == 200:
                print("✓ Login route accessible")
            else:
                print(f"✗ Login route returned status {response.status_code}")
                
            # Test redirect from root
            response = client.get('/')
            if response.status_code in [302, 200]:
                print("✓ Root route working (redirect expected)")
            else:
                print(f"✗ Root route returned unexpected status {response.status_code}")
                
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        
        # Check required config attributes
        required_attrs = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'SQLALCHEMY_TRACK_MODIFICATIONS']
        
        for attr in required_attrs:
            if hasattr(Config, attr):
                print(f"✓ Config attribute '{attr}' found")
            else:
                print(f"✗ Config attribute '{attr}' missing")
                return False
                
    except Exception as e:
        print(f"✗ Config testing error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("ClinicCare WebApp - Structure Validation Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_app_creation,
        test_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! ClinicCare app structure is valid.")
        print("\nNext steps:")
        print("1. Set up your MySQL database")
        print("2. Update .env file with your database credentials")
        print("3. Run: python app.py")
        print("4. Access the app at http://localhost:5000")
        print("5. Login with admin@cliniccare.com / admin123")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())