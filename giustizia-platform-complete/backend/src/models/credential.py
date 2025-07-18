from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from src.models.user import db
import json

class Credential(db.Model):
    __tablename__ = 'credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Nome identificador da credencial
    uuid = db.Column(db.String(255), nullable=False, unique=True)
    token = db.Column(db.Text, nullable=False)  # Criptografado
    device_name = db.Column(db.String(100), nullable=False)
    device_width = db.Column(db.String(10), nullable=False)
    device_height = db.Column(db.String(10), nullable=False)
    platform = db.Column(db.String(20), default='iOS 12.1')
    version = db.Column(db.String(20), default='1.1.13')
    
    # Controle de rate limiting
    last_used = db.Column(db.DateTime, nullable=True)
    requests_this_minute = db.Column(db.Integer, default=0)
    minute_window_start = db.Column(db.DateTime, nullable=True)
    max_requests_per_minute = db.Column(db.Integer, default=60)
    
    # Status e estatísticas
    is_active = db.Column(db.Boolean, default=True)
    total_requests = db.Column(db.Integer, default=0)
    successful_requests = db.Column(db.Integer, default=0)
    failed_requests = db.Column(db.Integer, default=0)
    average_response_time = db.Column(db.Float, default=0.0)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_error = db.Column(db.Text, nullable=True)
    last_error_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamento com histórico de consultas
    query_history = db.relationship('QueryHistory', backref='credential', lazy=True)
    
    def __repr__(self):
        return f'<Credential {self.name} - {self.uuid[:8]}...>'
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'name': self.name,
            'device_name': self.device_name,
            'device_width': self.device_width,
            'device_height': self.device_height,
            'platform': self.platform,
            'version': self.version,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'requests_this_minute': self.requests_this_minute,
            'max_requests_per_minute': self.max_requests_per_minute,
            'is_active': self.is_active,
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'average_response_time': self.average_response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_error': self.last_error,
            'last_error_at': self.last_error_at.isoformat() if self.last_error_at else None
        }
        
        if include_sensitive:
            data.update({
                'uuid': self.uuid,
                'token': self.token
            })
        
        return data
    
    def can_make_request(self):
        """Verifica se a credencial pode fazer uma nova requisição"""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        
        # Reset contador se passou mais de 1 minuto
        if (self.minute_window_start is None or 
            now - self.minute_window_start >= timedelta(minutes=1)):
            self.minute_window_start = now
            self.requests_this_minute = 0
            db.session.commit()
        
        return self.requests_this_minute < self.max_requests_per_minute
    
    def record_request(self, success=True, response_time=None, error_message=None):
        """Registra uma requisição feita com esta credencial"""
        now = datetime.utcnow()
        
        # Atualiza contadores
        self.last_used = now
        self.total_requests += 1
        self.requests_this_minute += 1
        
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            self.last_error = error_message
            self.last_error_at = now
        
        # Atualiza tempo médio de resposta
        if response_time is not None and success:
            if self.average_response_time == 0:
                self.average_response_time = response_time
            else:
                # Média móvel simples
                self.average_response_time = (self.average_response_time * 0.9) + (response_time * 0.1)
        
        self.updated_at = now
        db.session.commit()
    
    def get_request_parameters(self, process_number, process_year):
        """Retorna os parâmetros formatados para requisição à API"""
        return {
            "version": self.version,
            "platform": self.platform,
            "uuid": self.uuid,
            "devicename": self.device_name,
            "devicewidth": self.device_width,
            "deviceheight": self.device_height,
            "token": self.token,
            "azione": "direttarg_sicid_mobile",
            "registro": "CC",
            "idufficio": "958010098",
            "numproc": process_number,
            "aaproc": str(process_year),
            "tipoufficio": "1",
            "_": str(int(datetime.utcnow().timestamp() * 1000))
        }

