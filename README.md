# Job Tracker

A full-stack web application for tracking job applications and managing resumes, built with Django REST Framework backend and React frontend.

## Features

- **Job Application Management**: Track job applications with company, position, status, dates, and notes
- **Resume Management**: Upload, store, and manage multiple resume versions
- **Dashboard**: Overview of application statistics and recent activity
- **Status Tracking**: Track applications through different stages (Applied, Interview, Rejected, Accepted, Withdrawn)
- **Responsive Design**: Modern, mobile-friendly interface

## Project Structure

```
job-tracker/
├── backend/                # Django project
│   ├── jobtracker/         # Django project settings
│   ├── job_tracker/        # Consolidated Django app (applications + resumes)
│   ├── requirements.txt    # Python dependencies
│   └── manage.py
│
└── frontend/               # React project
    ├── public/
    ├── src/
    │   ├── components/     # React UI components
    │   ├── pages/          # Full page views
    │   ├── services/       # API calls to Django
    │   ├── App.js
    │   └── index.js
    └── package.json
```

## Quick Start

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

The Django API will be available at `http://localhost:8000`

### Frontend Setup (React)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
3. Install dependencies:
   ```bash
 npm install react-confetti   ```
  


4. Start the development server:
   ```bash
   npm start
   ```

   

The React app will be available at `http://localhost:3000`

## API Endpoints

### Job Applications
- `GET /api/applications/` - List all applications
- `POST /api/applications/` - Create new application
- `GET /api/applications/{id}/` - Get application details
- `PUT /api/applications/{id}/` - Update application
- `DELETE /api/applications/{id}/` - Delete application
- `GET /api/applications/stats/` - Get application statistics
- `GET /api/applications/recent/` - Get recent applications

### Resumes
- `GET /api/resumes/` - List all resumes
- `POST /api/resumes/` - Upload new resume
- `GET /api/resumes/{id}/` - Get resume details
- `PUT /api/resumes/{id}/` - Update resume
- `DELETE /api/resumes/{id}/` - Delete resume
- `POST /api/resumes/{id}/set_default/` - Set resume as default
- `GET /api/resumes/default/` - Get default resume

## Technologies Used

### Backend
- Django 4.2
- Django REST Framework
- Django CORS Headers
- SQLite (default database)

### Frontend
- React 18
- React Router DOM
- Axios for API calls
- Modern CSS with responsive design

## Development

### Adding New Features

1. **Backend**: Add models, serializers, and views in the appropriate Django app
2. **Frontend**: Create components and pages in the React app
3. **API Integration**: Update services to connect frontend to backend

### Database

The project uses SQLite by default for development. For production, consider using PostgreSQL:

1. Install PostgreSQL
2. Update `DATABASES` setting in `settings.py`
3. Install `psycopg2` adapter

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
