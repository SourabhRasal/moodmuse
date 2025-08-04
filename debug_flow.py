#!/usr/bin/env python3
"""
ClinicCare WebApp - Complete Debug Flow Simulation
This script simulates the entire application flow with sample data
and shows how the outputs would look in the actual application.
"""

import json
import random
from datetime import datetime, timedelta, date
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# Simulate database models with dataclasses
@dataclass
class User:
    user_id: int
    name: str
    email: str
    password_hash: str
    role: str
    created_at: datetime
    
    def is_admin(self):
        return self.role == 'admin'

@dataclass
class Patient:
    patient_id: int
    doctor_id: int
    name: str
    age: int
    gender: str
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime
    
    def get_visit_count(self, visits):
        return len([v for v in visits if v.patient_id == self.patient_id])
    
    def get_latest_visit(self, visits):
        patient_visits = [v for v in visits if v.patient_id == self.patient_id]
        return max(patient_visits, key=lambda v: v.date) if patient_visits else None

@dataclass
class Visit:
    visit_id: int
    patient_id: int
    doctor_id: int
    date: datetime
    symptoms: str
    prescription: Optional[str]
    follow_up_required: bool
    follow_up_date: Optional[date]
    notes: Optional[str]
    created_at: datetime

class ClinicCareDebugger:
    def __init__(self):
        self.users = []
        self.patients = []
        self.visits = []
        self.current_user = None
        
    def generate_sample_data(self):
        """Generate realistic sample data for testing"""
        print("🔄 Generating sample data...")
        
        # Create users
        self.users = [
            User(1, "Admin User", "admin@cliniccare.com", "hashed_admin123", "admin", datetime.now() - timedelta(days=30)),
            User(2, "Dr. Sarah Johnson", "sarah.johnson@cliniccare.com", "hashed_doctor123", "doctor", datetime.now() - timedelta(days=25)),
            User(3, "Dr. Michael Chen", "michael.chen@cliniccare.com", "hashed_doctor123", "doctor", datetime.now() - timedelta(days=20)),
            User(4, "Dr. Emily Davis", "emily.davis@cliniccare.com", "hashed_doctor123", "doctor", datetime.now() - timedelta(days=15)),
        ]
        
        # Create patients
        patient_names = [
            "John Smith", "Mary Johnson", "Robert Brown", "Patricia Miller", "James Wilson",
            "Jennifer Moore", "Michael Taylor", "Linda Anderson", "William Thomas", "Elizabeth Jackson",
            "David White", "Barbara Harris", "Richard Martin", "Susan Thompson", "Joseph Garcia",
            "Nancy Martinez", "Thomas Robinson", "Lisa Clark", "Christopher Rodriguez", "Karen Lewis"
        ]
        
        genders = ["Male", "Female", "Other"]
        
        for i, name in enumerate(patient_names):
            patient = Patient(
                patient_id=i+1,
                doctor_id=random.choice([2, 3, 4]),  # Assign to doctors only
                name=name,
                age=random.randint(18, 85),
                gender=random.choice(genders),
                phone=f"+1 (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                address=f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Pine Rd', 'Elm Dr'])}, City, State {random.randint(10000, 99999)}",
                created_at=datetime.now() - timedelta(days=random.randint(1, 90))
            )
            self.patients.append(patient)
        
        # Create visits
        symptoms_list = [
            "Fever and headache", "Persistent cough", "Chest pain", "Abdominal pain",
            "Back pain", "Fatigue and weakness", "Nausea and vomiting", "Dizziness",
            "Shortness of breath", "Joint pain", "Skin rash", "Sore throat",
            "High blood pressure", "Diabetes check-up", "Routine physical exam"
        ]
        
        prescriptions_list = [
            "Ibuprofen 400mg twice daily", "Amoxicillin 500mg three times daily",
            "Lisinopril 10mg once daily", "Metformin 500mg twice daily",
            "Aspirin 81mg once daily", "Acetaminophen 650mg as needed",
            "Prednisone 20mg for 5 days", "Omeprazole 20mg once daily"
        ]
        
        visit_id = 1
        for patient in self.patients:
            # Each patient has 1-5 visits
            num_visits = random.randint(1, 5)
            for _ in range(num_visits):
                visit_date = datetime.now() - timedelta(days=random.randint(1, 180))
                follow_up = random.choice([True, False])
                
                visit = Visit(
                    visit_id=visit_id,
                    patient_id=patient.patient_id,
                    doctor_id=patient.doctor_id,
                    date=visit_date,
                    symptoms=random.choice(symptoms_list),
                    prescription=random.choice(prescriptions_list) if random.choice([True, False]) else None,
                    follow_up_required=follow_up,
                    follow_up_date=visit_date.date() + timedelta(days=random.randint(7, 30)) if follow_up else None,
                    notes=f"Patient showed improvement. {random.choice(['Continue current treatment', 'Monitor symptoms', 'Schedule follow-up'])}" if random.choice([True, False]) else None,
                    created_at=visit_date
                )
                self.visits.append(visit)
                visit_id += 1
        
        print(f"✅ Generated {len(self.users)} users, {len(self.patients)} patients, {len(self.visits)} visits")
    
    def simulate_login(self, email: str):
        """Simulate user login"""
        print(f"\n🔐 LOGIN SIMULATION")
        print(f"Email: {email}")
        
        user = next((u for u in self.users if u.email == email), None)
        if user:
            self.current_user = user
            print(f"✅ Login successful - {user.name} ({user.role})")
            return True
        else:
            print("❌ Invalid credentials")
            return False
    
    def show_dashboard_data(self):
        """Show dashboard statistics"""
        print(f"\n📊 DASHBOARD DATA ({self.current_user.name})")
        print("=" * 50)
        
        if self.current_user.is_admin():
            total_patients = len(self.patients)
            total_visits = len(self.visits)
            total_doctors = len([u for u in self.users if u.role == 'doctor'])
        else:
            total_patients = len([p for p in self.patients if p.doctor_id == self.current_user.user_id])
            total_visits = len([v for v in self.visits if v.doctor_id == self.current_user.user_id])
            total_doctors = None
        
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_visits = len([v for v in self.visits 
                           if v.date >= seven_days_ago and 
                           (self.current_user.is_admin() or v.doctor_id == self.current_user.user_id)])
        
        follow_ups_pending = len([v for v in self.visits 
                                if v.follow_up_required and v.follow_up_date and v.follow_up_date <= date.today() and
                                (self.current_user.is_admin() or v.doctor_id == self.current_user.user_id)])
        
        print(f"Total Patients: {total_patients}")
        print(f"Total Visits: {total_visits}")
        if total_doctors:
            print(f"Total Doctors: {total_doctors}")
        print(f"Recent Visits (7 days): {recent_visits}")
        print(f"Follow-ups Pending: {follow_ups_pending}")
        
        # Latest patients
        if self.current_user.is_admin():
            latest_patients = sorted(self.patients, key=lambda p: p.created_at, reverse=True)[:5]
        else:
            latest_patients = sorted([p for p in self.patients if p.doctor_id == self.current_user.user_id], 
                                   key=lambda p: p.created_at, reverse=True)[:5]
        
        print(f"\nLatest Patients:")
        for patient in latest_patients:
            visit_count = patient.get_visit_count(self.visits)
            print(f"  • {patient.name} ({patient.age}y {patient.gender}) - {visit_count} visits")
    
    def show_patient_list(self):
        """Show patient list with pagination simulation"""
        print(f"\n👥 PATIENT LIST ({self.current_user.name})")
        print("=" * 80)
        
        if self.current_user.is_admin():
            patients = self.patients
        else:
            patients = [p for p in self.patients if p.doctor_id == self.current_user.user_id]
        
        print(f"{'Name':<20} {'Age':<5} {'Gender':<8} {'Phone':<15} {'Visits':<8} {'Latest Visit':<15}")
        print("-" * 80)
        
        for patient in patients[:10]:  # Show first 10 patients
            visit_count = patient.get_visit_count(self.visits)
            latest_visit = patient.get_latest_visit(self.visits)
            latest_date = latest_visit.date.strftime('%b %d, %Y') if latest_visit else 'No visits'
            
            print(f"{patient.name:<20} {patient.age:<5} {patient.gender:<8} {patient.phone:<15} {visit_count:<8} {latest_date:<15}")
        
        if len(patients) > 10:
            print(f"\n... and {len(patients) - 10} more patients")
    
    def show_patient_detail(self, patient_id: int):
        """Show detailed patient information"""
        patient = next((p for p in self.patients if p.patient_id == patient_id), None)
        if not patient:
            print(f"❌ Patient {patient_id} not found")
            return
        
        # Check access permissions
        if not self.current_user.is_admin() and patient.doctor_id != self.current_user.user_id:
            print(f"❌ Access denied to patient {patient.name}")
            return
        
        print(f"\n🏥 PATIENT DETAILS: {patient.name}")
        print("=" * 60)
        
        print(f"Patient ID: {patient.patient_id}")
        print(f"Name: {patient.name}")
        print(f"Age: {patient.age} years old")
        print(f"Gender: {patient.gender}")
        print(f"Phone: {patient.phone}")
        print(f"Address: {patient.address}")
        
        # Find doctor
        doctor = next((u for u in self.users if u.user_id == patient.doctor_id), None)
        print(f"Doctor: {doctor.name if doctor else 'Unknown'}")
        print(f"Registered: {patient.created_at.strftime('%B %d, %Y')}")
        
        # Visit history
        patient_visits = [v for v in self.visits if v.patient_id == patient.patient_id]
        patient_visits.sort(key=lambda v: v.date, reverse=True)
        
        print(f"\n📅 VISIT HISTORY ({len(patient_visits)} visits):")
        print("-" * 60)
        
        for visit in patient_visits:
            print(f"\n🗓️  {visit.date.strftime('%B %d, %Y at %I:%M %p')}")
            if visit.follow_up_required:
                print(f"   ⚠️  Follow-up Required")
            print(f"   Symptoms: {visit.symptoms}")
            if visit.prescription:
                print(f"   💊 Prescription: {visit.prescription}")
            if visit.follow_up_date:
                print(f"   📅 Follow-up Date: {visit.follow_up_date.strftime('%B %d, %Y')}")
            if visit.notes:
                print(f"   📝 Notes: {visit.notes}")
    
    def show_analytics_data(self):
        """Show analytics dashboard data"""
        print(f"\n📈 ANALYTICS DATA ({self.current_user.name})")
        print("=" * 60)
        
        # Filter visits based on user role
        if self.current_user.is_admin():
            filtered_visits = self.visits
            filtered_patients = self.patients
        else:
            filtered_visits = [v for v in self.visits if v.doctor_id == self.current_user.user_id]
            filtered_patients = [p for p in self.patients if p.doctor_id == self.current_user.user_id]
        
        # Visit trends (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_visits = [v for v in filtered_visits if v.date >= thirty_days_ago]
        
        print(f"📊 Visit Trends (Last 30 days): {len(recent_visits)} visits")
        
        # Group by date
        date_counts = {}
        for visit in recent_visits:
            date_key = visit.date.date()
            date_counts[date_key] = date_counts.get(date_key, 0) + 1
        
        print("Daily breakdown:")
        for date_key in sorted(date_counts.keys(), reverse=True)[:7]:  # Show last 7 days
            print(f"  {date_key.strftime('%b %d')}: {date_counts[date_key]} visits")
        
        # Gender distribution
        gender_counts = {}
        for patient in filtered_patients:
            gender_counts[patient.gender] = gender_counts.get(patient.gender, 0) + 1
        
        print(f"\n👥 Gender Distribution:")
        for gender, count in gender_counts.items():
            percentage = (count / len(filtered_patients)) * 100 if filtered_patients else 0
            print(f"  {gender}: {count} ({percentage:.1f}%)")
        
        # Age groups
        age_groups = {'0-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0}
        for patient in filtered_patients:
            if patient.age <= 18:
                age_groups['0-18'] += 1
            elif patient.age <= 35:
                age_groups['19-35'] += 1
            elif patient.age <= 50:
                age_groups['36-50'] += 1
            elif patient.age <= 65:
                age_groups['51-65'] += 1
            else:
                age_groups['65+'] += 1
        
        print(f"\n🎂 Age Group Distribution:")
        for age_group, count in age_groups.items():
            percentage = (count / len(filtered_patients)) * 100 if filtered_patients else 0
            print(f"  {age_group}: {count} ({percentage:.1f}%)")
        
        # Follow-up rates
        total_visits = len(filtered_visits)
        follow_up_visits = len([v for v in filtered_visits if v.follow_up_required])
        
        print(f"\n🔄 Follow-up Requirements:")
        print(f"  Follow-up Required: {follow_up_visits}")
        print(f"  No Follow-up: {total_visits - follow_up_visits}")
        if total_visits > 0:
            follow_up_rate = (follow_up_visits / total_visits) * 100
            print(f"  Follow-up Rate: {follow_up_rate:.1f}%")
    
    def show_admin_data(self):
        """Show admin-specific data"""
        if not self.current_user.is_admin():
            print("❌ Access denied - Admin privileges required")
            return
        
        print(f"\n🛡️  ADMIN DASHBOARD")
        print("=" * 60)
        
        # User statistics
        total_users = len(self.users)
        total_doctors = len([u for u in self.users if u.role == 'doctor'])
        total_admins = len([u for u in self.users if u.role == 'admin'])
        
        print(f"👥 User Management:")
        print(f"  Total Users: {total_users}")
        print(f"  Doctors: {total_doctors}")
        print(f"  Admins: {total_admins}")
        
        # System statistics
        print(f"\n📊 System Statistics:")
        print(f"  Total Patients: {len(self.patients)}")
        print(f"  Total Visits: {len(self.visits)}")
        
        # Recent activity
        recent_users = sorted(self.users, key=lambda u: u.created_at, reverse=True)[:5]
        print(f"\n🆕 Recent Users:")
        for user in recent_users:
            print(f"  • {user.name} ({user.role}) - {user.created_at.strftime('%b %d, %Y')}")
        
        # Doctor performance
        print(f"\n⭐ Doctor Activity:")
        for doctor in [u for u in self.users if u.role == 'doctor']:
            doctor_patients = len([p for p in self.patients if p.doctor_id == doctor.user_id])
            doctor_visits = len([v for v in self.visits if v.doctor_id == doctor.user_id])
            print(f"  • {doctor.name}: {doctor_patients} patients, {doctor_visits} visits")
    
    def simulate_form_submission(self, form_type: str, data: dict):
        """Simulate form submissions"""
        print(f"\n📝 FORM SUBMISSION: {form_type}")
        print("=" * 50)
        
        if form_type == "new_patient":
            print("Creating new patient...")
            patient_id = len(self.patients) + 1
            patient = Patient(
                patient_id=patient_id,
                doctor_id=self.current_user.user_id,
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                phone=data.get('phone'),
                address=data.get('address'),
                created_at=datetime.now()
            )
            self.patients.append(patient)
            print(f"✅ Patient '{patient.name}' created successfully (ID: {patient_id})")
            return patient_id
        
        elif form_type == "new_visit":
            print("Recording new visit...")
            visit_id = len(self.visits) + 1
            visit = Visit(
                visit_id=visit_id,
                patient_id=data['patient_id'],
                doctor_id=self.current_user.user_id,
                date=data['date'],
                symptoms=data['symptoms'],
                prescription=data.get('prescription'),
                follow_up_required=data.get('follow_up_required', False),
                follow_up_date=data.get('follow_up_date'),
                notes=data.get('notes'),
                created_at=datetime.now()
            )
            self.visits.append(visit)
            print(f"✅ Visit recorded successfully (ID: {visit_id})")
            return visit_id
    
    def simulate_search(self, query: str):
        """Simulate patient search"""
        print(f"\n🔍 SEARCH RESULTS for '{query}'")
        print("=" * 50)
        
        if self.current_user.is_admin():
            searchable_patients = self.patients
        else:
            searchable_patients = [p for p in self.patients if p.doctor_id == self.current_user.user_id]
        
        results = [p for p in searchable_patients if query.lower() in p.name.lower()]
        
        if results:
            print(f"Found {len(results)} patient(s):")
            for patient in results:
                visit_count = patient.get_visit_count(self.visits)
                print(f"  • {patient.name} ({patient.age}y {patient.gender}) - {visit_count} visits")
        else:
            print("No patients found matching the search criteria.")
        
        return results

def main():
    """Main debug flow"""
    debugger = ClinicCareDebugger()
    
    print("🏥 ClinicCare WebApp - Complete Debug Flow")
    print("=" * 60)
    
    # Step 1: Generate sample data
    debugger.generate_sample_data()
    
    # Step 2: Simulate doctor login
    print("\n" + "="*60)
    print("SCENARIO 1: DOCTOR LOGIN AND WORKFLOW")
    print("="*60)
    
    debugger.simulate_login("sarah.johnson@cliniccare.com")
    debugger.show_dashboard_data()
    debugger.show_patient_list()
    
    # Step 3: Show patient detail
    debugger.show_patient_detail(1)
    
    # Step 4: Simulate form submissions
    new_patient_data = {
        'name': 'Jane Doe',
        'age': 32,
        'gender': 'Female',
        'phone': '+1 (555) 123-4567',
        'address': '123 Main St, City, State 12345'
    }
    patient_id = debugger.simulate_form_submission("new_patient", new_patient_data)
    
    new_visit_data = {
        'patient_id': patient_id,
        'date': datetime.now(),
        'symptoms': 'Annual check-up, feeling well',
        'prescription': 'Vitamin D 1000IU daily',
        'follow_up_required': True,
        'follow_up_date': date.today() + timedelta(days=365),
        'notes': 'Patient in good health, continue current lifestyle'
    }
    debugger.simulate_form_submission("new_visit", new_visit_data)
    
    # Step 5: Show analytics
    debugger.show_analytics_data()
    
    # Step 6: Simulate search
    debugger.simulate_search("John")
    
    # Step 7: Admin workflow
    print("\n" + "="*60)
    print("SCENARIO 2: ADMIN LOGIN AND WORKFLOW")
    print("="*60)
    
    debugger.simulate_login("admin@cliniccare.com")
    debugger.show_dashboard_data()
    debugger.show_admin_data()
    debugger.show_analytics_data()
    
    # Step 8: Show JSON data structure (how data would be stored)
    print("\n" + "="*60)
    print("DATABASE STRUCTURE SIMULATION")
    print("="*60)
    
    print("\n📊 Sample Data Structures:")
    
    sample_user = debugger.users[1]  # Doctor
    print(f"\n🔹 User Model:")
    print(json.dumps(asdict(sample_user), indent=2, default=str))
    
    sample_patient = debugger.patients[0]
    print(f"\n🔹 Patient Model:")
    print(json.dumps(asdict(sample_patient), indent=2, default=str))
    
    sample_visit = debugger.visits[0]
    print(f"\n🔹 Visit Model:")
    print(json.dumps(asdict(sample_visit), indent=2, default=str))
    
    print("\n" + "="*60)
    print("🎉 DEBUG FLOW COMPLETE!")
    print("="*60)
    print("This simulation shows exactly how the ClinicCare WebApp")
    print("would function with real data in a production environment.")

if __name__ == "__main__":
    main()