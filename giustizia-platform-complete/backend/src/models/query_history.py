from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class QueryHistory(db.Model):
    __tablename__ = 'query_history'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False, index=True)
    credential_id = db.Column(db.Integer, db.ForeignKey('credentials.id'), nullable=True, index=True)
    query_timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    response_status = db.Column(db.String(20), nullable=False)  # 'success', 'error', 'rate_limited'
    response_time_ms = db.Column(db.Integer, nullable=True)
    status_result = db.Column(db.Text, nullable=True)
    raw_response = db.Column(db.Text, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    status_changed = db.Column(db.Boolean, default=False)
    previous_status = db.Column(db.Text, nullable=True)
    
    # Índices para otimizar consultas
    __table_args__ = (
        db.Index('idx_client_timestamp', 'client_id', 'query_timestamp'),
        db.Index('idx_credential_timestamp', 'credential_id', 'query_timestamp'),
        db.Index('idx_response_status', 'response_status'),
    )
    
    def __repr__(self):
        return f'<QueryHistory Client:{self.client_id} - {self.query_timestamp} - {self.response_status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'credential_id': self.credential_id,
            'query_timestamp': self.query_timestamp.isoformat() if self.query_timestamp else None,
            'response_status': self.response_status,
            'response_time_ms': self.response_time_ms,
            'status_result': self.status_result,
            'error_message': self.error_message,
            'status_changed': self.status_changed,
            'previous_status': self.previous_status
        }

