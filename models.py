from app import db
from datetime import datetime, date
from sqlalchemy import func


class Personnel(db.Model):
    __tablename__ = 'personnel'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    joining_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def days(self):
        """Calculate days since joining"""
        return (date.today() - self.joining_date).days
    
    def __repr__(self):
        return f'<Personnel {self.name} - {self.platform}>'


# Platform and position configuration
PLATFORM_POSITIONS = {
    "BHS": ["Technician 1", "Technician 2", "Technician 3", "Technician 4", "Technician 5", "Service engineering"],
    "SCA": ["Technician 1", "Technician 2"],
    "ICP": ["Technician 1", "Technician 2", "Technician 3", "Technician 4", "Service engineering"],
    "SHP": ["Technician 1", "Technician 2", "Technician 3", "Technician 4", "Service engineering"],
    "MHN": ["Technician 1", "Technician 2", "Technician 3", "Technician 4", "Service engineering"],
    "NQ": ["Technician 1", "Technician 2", "Technician 3", "Technician 4", "Service engineering"],
    "WIN": ["Technician 1", "Technician 2"],
    "BPA": ["Technician 1", "Technician 2", "Technician 3", "Service engineering"],
    "BPB": ["Technician 1", "Technician 2", "Technician 3", "Service engineering"],
    "B-193": ["Technician 1", "Technician 2"],
    "TAPTI": ["Technician 1", "Technician 2"],
    "PANNA": ["Technician 1", "Technician 2"],
    "D1": ["Technician 1", "Technician 2"],
    "NEELAM": ["Technician 1", "Technician 2", "Service engineering"],
    "HEERA": ["Technician 1", "Technician 2", "Service engineering"],
    "RATNA": ["Technician 1", "Technician 2", "Service engineering"],
    "SAGAR GAURAV": ["Technician 1", "Technician 2"],
    "SAGAR SHAKTI": ["Technician 1", "Technician 2"],
    "SAGAR JYOUTI": ["Technician 1", "Technician 2"],
    "SAGAR KRIAN": ["Technician 1", "Technician 2"],
    "SAGAR RATNA": ["Technician 1", "Technician 2"],
    "SAGAR UDAY": ["Technician 1", "Technician 2"],
}

# Maximum personnel per position (1 person per position per platform)
MAX_PERSONNEL_PER_POSITION = {
    "Technician 1": 1,
    "Technician 2": 1,
    "Technician 3": 1,
    "Technician 4": 1,
    "Technician 5": 1,
    "Service engineering": 1,
}
