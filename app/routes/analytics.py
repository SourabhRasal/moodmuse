from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Patient, Visit, User
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import pandas as pd
import plotly.graph_objs as go
import plotly.utils

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def dashboard():
    return render_template('analytics/dashboard.html')

@analytics_bp.route('/api/visit-trends')
@login_required
def visit_trends():
    # Get visit trends for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    if current_user.is_admin():
        visits = db.session.query(
            func.date(Visit.date).label('date'),
            func.count(Visit.visit_id).label('count')
        ).filter(Visit.date >= thirty_days_ago).group_by(func.date(Visit.date)).all()
    else:
        visits = db.session.query(
            func.date(Visit.date).label('date'),
            func.count(Visit.visit_id).label('count')
        ).filter(
            Visit.doctor_id == current_user.user_id,
            Visit.date >= thirty_days_ago
        ).group_by(func.date(Visit.date)).all()
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame([(v.date, v.count) for v in visits], columns=['date', 'count'])
    
    # Create date range and fill missing dates with 0
    date_range = pd.date_range(start=thirty_days_ago.date(), end=datetime.utcnow().date())
    df_complete = pd.DataFrame({'date': date_range})
    df_complete['date'] = df_complete['date'].dt.date
    df = df_complete.merge(df, on='date', how='left').fillna(0)
    
    # Create Plotly figure
    fig = go.Figure(data=go.Scatter(
        x=df['date'],
        y=df['count'],
        mode='lines+markers',
        name='Daily Visits',
        line=dict(color='#007bff', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Daily Visit Trends (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='Number of Visits',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))

@analytics_bp.route('/api/gender-distribution')
@login_required
def gender_distribution():
    if current_user.is_admin():
        gender_data = db.session.query(
            Patient.gender,
            func.count(Patient.patient_id).label('count')
        ).group_by(Patient.gender).all()
    else:
        gender_data = db.session.query(
            Patient.gender,
            func.count(Patient.patient_id).label('count')
        ).filter(Patient.doctor_id == current_user.user_id).group_by(Patient.gender).all()
    
    labels = [g.gender for g in gender_data]
    values = [g.count for g in gender_data]
    
    fig = go.Figure(data=go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ))
    
    fig.update_layout(
        title='Patient Gender Distribution',
        template='plotly_white'
    )
    
    return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))

@analytics_bp.route('/api/age-groups')
@login_required
def age_groups():
    if current_user.is_admin():
        patients = Patient.query.all()
    else:
        patients = Patient.query.filter_by(doctor_id=current_user.user_id).all()
    
    # Create age groups
    age_groups = {'0-18': 0, '19-35': 0, '36-50': 0, '51-65': 0, '65+': 0}
    
    for patient in patients:
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
    
    fig = go.Figure(data=go.Bar(
        x=list(age_groups.keys()),
        y=list(age_groups.values()),
        marker=dict(color='#45B7D1')
    ))
    
    fig.update_layout(
        title='Patient Age Group Distribution',
        xaxis_title='Age Groups',
        yaxis_title='Number of Patients',
        template='plotly_white'
    )
    
    return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))

@analytics_bp.route('/api/follow-up-rates')
@login_required
def follow_up_rates():
    if current_user.is_admin():
        total_visits = Visit.query.count()
        follow_up_visits = Visit.query.filter(Visit.follow_up_required == True).count()
    else:
        total_visits = Visit.query.filter_by(doctor_id=current_user.user_id).count()
        follow_up_visits = Visit.query.filter(
            Visit.doctor_id == current_user.user_id,
            Visit.follow_up_required == True
        ).count()
    
    no_follow_up = total_visits - follow_up_visits
    
    fig = go.Figure(data=go.Pie(
        labels=['Follow-up Required', 'No Follow-up'],
        values=[follow_up_visits, no_follow_up],
        hole=0.4,
        marker=dict(colors=['#FF6B6B', '#4ECDC4'])
    ))
    
    fig.update_layout(
        title='Follow-up Requirements',
        template='plotly_white'
    )
    
    return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))

@analytics_bp.route('/api/monthly-visits')
@login_required
def monthly_visits():
    # Get visits for the last 12 months
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    
    if current_user.is_admin():
        monthly_data = db.session.query(
            extract('year', Visit.date).label('year'),
            extract('month', Visit.date).label('month'),
            func.count(Visit.visit_id).label('count')
        ).filter(Visit.date >= twelve_months_ago).group_by(
            extract('year', Visit.date),
            extract('month', Visit.date)
        ).order_by(
            extract('year', Visit.date),
            extract('month', Visit.date)
        ).all()
    else:
        monthly_data = db.session.query(
            extract('year', Visit.date).label('year'),
            extract('month', Visit.date).label('month'),
            func.count(Visit.visit_id).label('count')
        ).filter(
            Visit.doctor_id == current_user.user_id,
            Visit.date >= twelve_months_ago
        ).group_by(
            extract('year', Visit.date),
            extract('month', Visit.date)
        ).order_by(
            extract('year', Visit.date),
            extract('month', Visit.date)
        ).all()
    
    # Format data for chart
    months = []
    counts = []
    
    for data in monthly_data:
        month_name = datetime(int(data.year), int(data.month), 1).strftime('%b %Y')
        months.append(month_name)
        counts.append(data.count)
    
    fig = go.Figure(data=go.Bar(
        x=months,
        y=counts,
        marker=dict(color='#45B7D1')
    ))
    
    fig.update_layout(
        title='Monthly Visit Trends (Last 12 Months)',
        xaxis_title='Month',
        yaxis_title='Number of Visits',
        template='plotly_white'
    )
    
    return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))