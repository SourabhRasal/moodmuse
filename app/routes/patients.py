from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Patient, Visit, User
from app.forms import PatientForm, VisitForm
from datetime import datetime

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/')
@login_required
def list_patients():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    if current_user.is_admin():
        query = Patient.query
        if search:
            query = query.filter(Patient.name.contains(search))
    else:
        query = Patient.query.filter_by(doctor_id=current_user.user_id)
        if search:
            query = query.filter(Patient.name.contains(search))
    
    patients = query.order_by(Patient.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('patients/list.html', patients=patients, search=search)

@patients_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    
    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            phone=form.phone.data,
            address=form.address.data,
            doctor_id=current_user.user_id
        )
        db.session.add(patient)
        db.session.commit()
        flash(f'Patient {patient.name} has been added successfully!', 'success')
        return redirect(url_for('patients.view_patient', id=patient.patient_id))
    
    return render_template('patients/form.html', form=form, title='Add New Patient')

@patients_bp.route('/<int:id>')
@login_required
def view_patient(id):
    if current_user.is_admin():
        patient = Patient.query.get_or_404(id)
    else:
        patient = Patient.query.filter_by(patient_id=id, doctor_id=current_user.user_id).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    visits = Visit.query.filter_by(patient_id=id).order_by(Visit.date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('patients/detail.html', patient=patient, visits=visits)

@patients_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    if current_user.is_admin():
        patient = Patient.query.get_or_404(id)
    else:
        patient = Patient.query.filter_by(patient_id=id, doctor_id=current_user.user_id).first_or_404()
    
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.age = form.age.data
        patient.gender = form.gender.data
        patient.phone = form.phone.data
        patient.address = form.address.data
        db.session.commit()
        flash(f'Patient {patient.name} has been updated successfully!', 'success')
        return redirect(url_for('patients.view_patient', id=patient.patient_id))
    
    return render_template('patients/form.html', form=form, title='Edit Patient', patient=patient)

@patients_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_patient(id):
    if current_user.is_admin():
        patient = Patient.query.get_or_404(id)
    else:
        patient = Patient.query.filter_by(patient_id=id, doctor_id=current_user.user_id).first_or_404()
    
    name = patient.name
    db.session.delete(patient)
    db.session.commit()
    flash(f'Patient {name} has been deleted successfully!', 'success')
    return redirect(url_for('patients.list_patients'))

@patients_bp.route('/<int:id>/visit/new', methods=['GET', 'POST'])
@login_required
def new_visit(id):
    if current_user.is_admin():
        patient = Patient.query.get_or_404(id)
    else:
        patient = Patient.query.filter_by(patient_id=id, doctor_id=current_user.user_id).first_or_404()
    
    form = VisitForm()
    
    if form.validate_on_submit():
        visit = Visit(
            patient_id=patient.patient_id,
            doctor_id=current_user.user_id,
            date=form.date.data,
            symptoms=form.symptoms.data,
            prescription=form.prescription.data,
            follow_up_required=form.follow_up_required.data,
            follow_up_date=form.follow_up_date.data if form.follow_up_required.data else None,
            notes=form.notes.data
        )
        db.session.add(visit)
        db.session.commit()
        flash('Visit record has been added successfully!', 'success')
        return redirect(url_for('patients.view_patient', id=patient.patient_id))
    
    return render_template('patients/visit_form.html', form=form, patient=patient, title='Add New Visit')

@patients_bp.route('/visit/<int:visit_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_visit(visit_id):
    if current_user.is_admin():
        visit = Visit.query.get_or_404(visit_id)
    else:
        visit = Visit.query.filter_by(visit_id=visit_id, doctor_id=current_user.user_id).first_or_404()
    
    form = VisitForm(obj=visit)
    
    if form.validate_on_submit():
        visit.date = form.date.data
        visit.symptoms = form.symptoms.data
        visit.prescription = form.prescription.data
        visit.follow_up_required = form.follow_up_required.data
        visit.follow_up_date = form.follow_up_date.data if form.follow_up_required.data else None
        visit.notes = form.notes.data
        db.session.commit()
        flash('Visit record has been updated successfully!', 'success')
        return redirect(url_for('patients.view_patient', id=visit.patient_id))
    
    return render_template('patients/visit_form.html', form=form, patient=visit.patient, visit=visit, title='Edit Visit')

@patients_bp.route('/visit/<int:visit_id>/delete', methods=['POST'])
@login_required
def delete_visit(visit_id):
    if current_user.is_admin():
        visit = Visit.query.get_or_404(visit_id)
    else:
        visit = Visit.query.filter_by(visit_id=visit_id, doctor_id=current_user.user_id).first_or_404()
    
    patient_id = visit.patient_id
    db.session.delete(visit)
    db.session.commit()
    flash('Visit record has been deleted successfully!', 'success')
    return redirect(url_for('patients.view_patient', id=patient_id))