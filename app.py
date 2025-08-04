from app import create_app, db
from app.models import User, Patient, Visit

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Patient': Patient, 'Visit': Visit}

def init_db():
    """Initialize database with tables and create default admin user"""
    with app.app_context():
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(email='admin@cliniccare.com').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@cliniccare.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create sample doctor
            doctor = User(
                name='Dr. John Smith',
                email='doctor@cliniccare.com',
                role='doctor'
            )
            doctor.set_password('doctor123')
            db.session.add(doctor)
            
            db.session.commit()
            print("Database initialized with default users:")
            print("Admin: admin@cliniccare.com / admin123")
            print("Doctor: doctor@cliniccare.com / doctor123")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)