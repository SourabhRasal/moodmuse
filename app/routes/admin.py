from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Patient, Visit
from app.forms import RegistrationForm
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # System statistics
    total_users = User.query.count()
    total_doctors = User.query.filter_by(role='doctor').count()
    total_patients = Patient.query.count()
    total_visits = Visit.query.count()
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
    recent_visits = Visit.query.order_by(Visit.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_visits=total_visits,
                         recent_users=recent_users,
                         recent_patients=recent_patients,
                         recent_visits=recent_visits)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    if search:
        query = query.filter(User.name.contains(search) | User.email.contains(search))
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, search=search)

@admin_bp.route('/users/<int:id>')
@login_required
@admin_required
def view_user(id):
    user = User.query.get_or_404(id)
    
    # Get user's patients and visits statistics
    patient_count = Patient.query.filter_by(doctor_id=user.user_id).count()
    visit_count = Visit.query.filter_by(doctor_id=user.user_id).count()
    
    # Recent patients and visits
    recent_patients = Patient.query.filter_by(doctor_id=user.user_id)\
                                 .order_by(Patient.created_at.desc()).limit(5).all()
    recent_visits = Visit.query.filter_by(doctor_id=user.user_id)\
                              .order_by(Visit.created_at.desc()).limit(5).all()
    
    return render_template('admin/user_detail.html',
                         user=user,
                         patient_count=patient_count,
                         visit_count=visit_count,
                         recent_patients=recent_patients,
                         recent_visits=recent_visits)

@admin_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']
        
        if request.form.get('password'):
            user.set_password(request.form['password'])
        
        db.session.commit()
        flash(f'User {user.name} has been updated successfully!', 'success')
        return redirect(url_for('admin.view_user', id=user.user_id))
    
    return render_template('admin/user_form.html', user=user, title='Edit User')

@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    if user.user_id == current_user.user_id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.users'))
    
    name = user.name
    db.session.delete(user)
    db.session.commit()
    flash(f'User {name} has been deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/patients')
@login_required
@admin_required
def patients():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Patient.query.join(User)
    if search:
        query = query.filter(Patient.name.contains(search) | User.name.contains(search))
    
    patients = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/patients.html', patients=patients, search=search)

@admin_bp.route('/visits')
@login_required
@admin_required
def visits():
    page = request.args.get('page', 1, type=int)
    
    visits = Visit.query.join(Patient).join(User)\
                       .order_by(Visit.created_at.desc())\
                       .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/visits.html', visits=visits)