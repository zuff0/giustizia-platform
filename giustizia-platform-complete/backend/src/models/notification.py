from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True, index=True)
    notification_type = db.Column(db.String(50), nullable=False, index=True)  # 'status_change', 'error', 'system_alert'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='info')  # 'info', 'warning', 'error', 'success'
    
    # Dados específicos da notificação
    previous_status = db.Column(db.Text, nullable=True)
    new_status = db.Column(db.Text, nullable=True)
    process_number = db.Column(db.String(20), nullable=True)
    process_year = db.Column(db.Integer, nullable=True)
    
    # Status da notificação
    is_read = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    sent_to = db.Column(db.String(200), nullable=True)  # email ou outro destino
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relacionamento com cliente
    client = db.relationship('Client', backref='notifications', lazy=True)
    
    def __repr__(self):
        return f'<Notification {self.notification_type} - {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'severity': self.severity,
            'previous_status': self.previous_status,
            'new_status': self.new_status,
            'process_number': self.process_number,
            'process_year': self.process_year,
            'is_read': self.is_read,
            'is_sent': self.is_sent,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'sent_to': self.sent_to,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    def mark_as_read(self):
        """Marca a notificação como lida"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_sent(self, sent_to=None):
        """Marca a notificação como enviada"""
        self.is_sent = True
        self.sent_at = datetime.utcnow()
        if sent_to:
            self.sent_to = sent_to
        db.session.commit()
    
    @staticmethod
    def create_status_change_notification(client, previous_status, new_status):
        """Cria uma notificação de mudança de status"""
        notification = Notification(
            client_id=client.id,
            notification_type='status_change',
            title=f'Status alterado - Processo {client.process_number}/{client.process_year}',
            message=f'O status do processo de {client.name} foi alterado de "{previous_status}" para "{new_status}"',
            severity='info',
            previous_status=previous_status,
            new_status=new_status,
            process_number=client.process_number,
            process_year=client.process_year
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def create_error_notification(client, error_message):
        """Cria uma notificação de erro"""
        notification = Notification(
            client_id=client.id if client else None,
            notification_type='error',
            title=f'Erro na consulta - Processo {client.process_number}/{client.process_year}' if client else 'Erro no sistema',
            message=error_message,
            severity='error',
            process_number=client.process_number if client else None,
            process_year=client.process_year if client else None
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def create_system_alert(title, message, severity='warning'):
        """Cria um alerta do sistema"""
        notification = Notification(
            notification_type='system_alert',
            title=title,
            message=message,
            severity=severity
        )
        db.session.add(notification)
        db.session.commit()
        return notification

