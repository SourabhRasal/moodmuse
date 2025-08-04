# ClinicCare WebApp

A comprehensive clinic management system built with Flask, designed for doctors to manage patient records, track visits, and analyze practice trends.

## 🏥 Features

### Doctor Features
- **Patient Management**: Add, edit, delete, and search patient records
- **Visit Tracking**: Record detailed visit information with symptoms, prescriptions, and follow-ups
- **Analytics Dashboard**: Interactive charts showing visit trends, patient demographics, and follow-up rates
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Admin Features
- **User Management**: Create and manage doctor accounts
- **System Overview**: View all patients, visits, and user statistics
- **Full Data Access**: Access to all records across the system
- **Role-based Security**: Secure admin-only features

### Analytics & Insights
- Daily and monthly visit trends
- Patient age group and gender distribution
- Follow-up requirements tracking
- Interactive Plotly charts
- Exportable data visualizations

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: MySQL (compatible with Planetscale)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login with bcrypt password hashing
- **Data Visualization**: Plotly.js for interactive charts
- **Data Processing**: Pandas and NumPy for analytics
- **Deployment**: Render, Railway, or Heroku ready

## 📋 Requirements

- Python 3.8 or higher
- MySQL database
- Virtual environment (recommended)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cliniccare-webapp
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DB_USER=your-db-username
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_NAME=cliniccare
FLASK_ENV=development
```

### 5. Initialize Database
```bash
python app.py
```

This will create the database tables and add default users:
- **Admin**: `admin@cliniccare.com` / `admin123`
- **Doctor**: `doctor@cliniccare.com` / `doctor123`

### 6. Run the Application
```bash
python app.py
```

Access the application at `http://localhost:5000`

## 🗄️ Database Schema

### Users Table
- `user_id` (Primary Key)
- `name` (Full name)
- `email` (Unique email address)
- `password_hash` (Bcrypt hashed password)
- `role` (doctor/admin)
- `created_at` (Registration timestamp)

### Patients Table
- `patient_id` (Primary Key)
- `doctor_id` (Foreign Key to Users)
- `name` (Patient name)
- `age` (Patient age)
- `gender` (Male/Female/Other)
- `phone` (Optional contact number)
- `address` (Optional address)
- `created_at` (Registration timestamp)

### Visits Table
- `visit_id` (Primary Key)
- `patient_id` (Foreign Key to Patients)
- `doctor_id` (Foreign Key to Users)
- `date` (Visit date and time)
- `symptoms` (Patient symptoms)
- `prescription` (Prescribed medication)
- `follow_up_required` (Boolean)
- `follow_up_date` (Optional follow-up date)
- `notes` (Additional notes)
- `created_at` (Record creation timestamp)

## 🔐 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Flask-Login for secure user sessions
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Role-based Access**: Doctors can only access their own data
- **Form Validation**: Server-side validation for all inputs

## 📊 Analytics Features

The analytics dashboard provides:

1. **Visit Trends**: Line chart showing daily visits over the last 30 days
2. **Gender Distribution**: Pie chart of patient gender demographics
3. **Age Groups**: Bar chart showing patient age group distribution
4. **Follow-up Rates**: Pie chart of follow-up requirements
5. **Monthly Trends**: Bar chart showing visit counts by month

## 🚀 Deployment

### Render Deployment
1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service from your repository
4. Set environment variables in Render dashboard
5. Deploy with one click

### Railway Deployment
1. Install Railway CLI
2. Run `railway login`
3. Run `railway init`
4. Set environment variables with `railway variables`
5. Deploy with `railway up`

### Manual Deployment
1. Set up MySQL database (Planetscale recommended)
2. Configure environment variables
3. Run `python app.py` on your server
4. Configure reverse proxy (nginx recommended)

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |
| `DB_USER` | Database username | `root` |
| `DB_PASSWORD` | Database password | `password` |
| `DB_HOST` | Database host | `localhost` |
| `DB_NAME` | Database name | `cliniccare` |
| `FLASK_ENV` | Flask environment | `development` |

### Database Setup
For production, use a managed MySQL service like:
- [Planetscale](https://planetscale.com/) (Recommended)
- [Amazon RDS](https://aws.amazon.com/rds/)
- [Google Cloud SQL](https://cloud.google.com/sql)
- [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases/)

## 📱 User Interface

### Responsive Design
- Mobile-first approach
- Bootstrap 5 framework
- Dark mode support
- Accessibility compliant

### Key UI Components
- **Dashboard**: Overview with statistics cards
- **Patient List**: Searchable table with pagination
- **Patient Details**: Complete patient information and visit history
- **Forms**: Intuitive forms with validation feedback
- **Analytics**: Interactive charts and graphs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `docs/` folder
- Review the code comments for implementation details

## 🎯 Future Enhancements

- [ ] Patient appointment scheduling
- [ ] Medical report generation
- [ ] Integration with medical devices
- [ ] Telemedicine features
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] API for third-party integrations

---

**ClinicCare** - Simplifying clinic management, one patient at a time. 🏥✨