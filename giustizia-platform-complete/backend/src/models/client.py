from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    document_number = db.Column(db.String(50), nullable=True)
    process_number = db.Column(db.String(20), nullable=False, index=True)
    process_year = db.Column(db.Integer, nullable=False, index=True)
    current_status = db.Column(db.Text, nullable=True)
    last_status_check = db.Column(db.DateTime, nullable=True)
    last_status_change = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relacionamento com histórico de consultas
    query_history = db.relationship('QueryHistory', backref='client', lazy=True, cascade='all, delete-orphan')
    
    # Índice composto para otimizar consultas por processo
    __table_args__ = (
        db.Index('idx_process_number_year', 'process_number', 'process_year'),
    )
    
    def __repr__(self):
        return f'<Client {self.name} - Process {self.process_number}/{self.process_year}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'document_number': self.document_number,
            'process_number': self.process_number,
            'process_year': self.process_year,
            'current_status': self.current_status,
            'last_status_check': self.last_status_check.isoformat() if self.last_status_check else None,
            'last_status_change': self.last_status_change.isoformat() if self.last_status_change else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'notes': self.notes
        }
    
    def update_status(self, new_status):
        """Atualiza o status do cliente e registra a mudança se necessário"""
        if self.current_status != new_status:
            self.current_status = new_status
            self.last_status_change = datetime.utcnow()
        self.last_status_check = datetime.utcnow()
        self.updated_at = datetime.utcnow()

