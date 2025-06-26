# Personnel Management System

A Flask-based web application for managing personnel across oil & gas platforms and rigs, optimized for Railway hosting.

## Features

- **Personnel Management**: Add, track, and manage personnel across 22 platforms
- **Dashboard View**: Live overview of personnel deployment status
- **TV Dashboard**: Full-screen slideshow for monitoring displays
- **Platform Types**: Supports both regular platforms and SAGAR rigs
- **Shortage Tracking**: Automatic detection of position shortages
- **Critical Personnel**: Alerts for personnel over 100 days deployment
- **Admin Panel**: Complete management interface

## Platform Coverage

### Regular Platforms
- BHS, SCA, ICP, SHP, MHN, NQ, WIN, BPA
- BPB, B-193, TAPTI, PANNA, D1, NEELAM, HEERA, RATNA

### SAGAR Rigs
- SAGAR GAURAV, SAGAR SHAKTI, SAGAR JYOUTI
- SAGAR KRIAN, SAGAR RATNA, SAGAR UDAY

## Technician Positions
- Technician 1, Technician 2, Technician 3, Technician 4, Technician 5
- Service Engineering

## Railway Deployment

This application is optimized for Railway hosting with the following features:

### Environment Variables Required
- `DATABASE_URL`: PostgreSQL connection string (automatically provided by Railway)
- `SESSION_SECRET`: Random secret key for session security (auto-generated)

### Railway Configuration
- Uses `railway.toml` for deployment configuration
- Supports Railway's PostgreSQL service
- Configured for automatic restarts and proper port binding
- Optimized for Railway's container environment

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SESSION_SECRET`: Random secret key
3. Run: `python main.py`

### Railway Deployment Steps
1. Fork/clone this repository
2. Connect to Railway (https://railway.app)
3. Create new project from GitHub repository
4. Add PostgreSQL service to your project
5. Deploy - Railway will automatically:
   - Install dependencies from requirements.txt
   - Configure database connection
   - Generate session secret
   - Start the application with gunicorn

## Application Structure

- `app.py`: Flask application configuration and database setup
- `main.py`: Application entry point
- `models.py`: Database models and platform configurations
- `routes.py`: All application routes and business logic
- `templates/`: Jinja2 HTML templates
- `railway.toml`: Railway deployment configuration

## Usage

1. **Admin Panel**: Add personnel to platforms with specific positions
2. **Dashboard**: View current deployment status with color-coded alerts
3. **TV Dashboard**: Full-screen slideshow for monitoring rooms

## Technology Stack

- **Backend**: Flask 3.0.0, SQLAlchemy 2.0.23
- **Database**: PostgreSQL (Railway managed)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Railway with Gunicorn WSGI server
- **Python**: 3.11

## Database Schema

The application uses a single `Personnel` table with the following fields:
- `id`: Primary key
- `name`: Personnel full name
- `platform`: Assigned platform/rig
- `position`: Technical position
- `joining_date`: Date of deployment
- `created_at`: Record creation timestamp

## Security Features

- Environment-based configuration
- Session management with secure keys
- SQL injection protection via SQLAlchemy ORM
- Input validation and sanitization
- CSRF protection through Flask's built-in features

## Monitoring & Alerts

- **Color-coded status indicators**:
  - Green: ≤28 days (Good)
  - Yellow: 29-56 days (Caution)
  - Orange: 57-100 days (Warning)
  - Red: >100 days (Critical)

- **Shortage tracking**: Automatic detection of unfilled positions
- **TV Dashboard**: Auto-advancing slideshow for monitoring displays
- **Real-time statistics**: Personnel count, platform status, critical alerts

## License

Power Mech Services Pvt. Ltd. - Internal Use Only
