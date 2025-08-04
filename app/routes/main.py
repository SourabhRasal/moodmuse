from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Patient, Visit, User
from datetime import datetime, timedelta
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get statistics for the current doctor
    if current_user.is_admin():
        total_patients = Patient.query.count()
        total_visits = Visit.query.count()
        total_doctors = User.query.filter_by(role='doctor').count()
    else:
        total_patients = Patient.query.filter_by(doctor_id=current_user.user_id).count()
        total_visits = Visit.query.filter_by(doctor_id=current_user.user_id).count()
        total_doctors = None
    
    # Recent visits (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    if current_user.is_admin():
        recent_visits = Visit.query.filter(Visit.date >= seven_days_ago).count()
        follow_ups_pending = Visit.query.filter(
            Visit.follow_up_required == True,
            Visit.follow_up_date <= datetime.utcnow().date()
        ).count()
    else:
        recent_visits = Visit.query.filter(
            Visit.doctor_id == current_user.user_id,
            Visit.date >= seven_days_ago
        ).count()
        follow_ups_pending = Visit.query.filter(
            Visit.doctor_id == current_user.user_id,
            Visit.follow_up_required == True,
            Visit.follow_up_date <= datetime.utcnow().date()
        ).count()
    
    # Latest patients
    if current_user.is_admin():
        latest_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    else:
        latest_patients = Patient.query.filter_by(doctor_id=current_user.user_id)\
                                     .order_by(Patient.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html',
                         total_patients=total_patients,
                         total_visits=total_visits,
                         total_doctors=total_doctors,
                         recent_visits=recent_visits,
                         follow_ups_pending=follow_ups_pending,
                         latest_patients=latest_patients)