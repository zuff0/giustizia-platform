from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db
import json

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False, unique=True, index=True)
    value = db.Column(db.Text, nullable=False)
    value_type = db.Column(db.String(20), default='string')  # 'string', 'integer', 'float', 'boolean', 'json'
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='general', index=True)
    is_sensitive = db.Column(db.Boolean, default=False)  # Para valores que não devem ser expostos na API
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<SystemConfig {self.key}={self.value}>'
    
    def to_dict(self, include_sensitive=False):
        if self.is_sensitive and not include_sensitive:
            return {
                'id': self.id,
                'key': self.key,
                'value': '***HIDDEN***',
                'value_type': self.value_type,
                'description': self.description,
                'category': self.category,
                'is_sensitive': self.is_sensitive,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                'updated_by': self.updated_by
            }
        
        return {
            'id': self.id,
            'key': self.key,
            'value': self.get_typed_value(),
            'value_type': self.value_type,
            'description': self.description,
            'category': self.category,
            'is_sensitive': self.is_sensitive,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'updated_by': self.updated_by
        }
    
    def get_typed_value(self):
        """Retorna o valor convertido para o tipo apropriado"""
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'float':
            return float(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'json':
            return json.loads(self.value)
        else:
            return self.value
    
    def set_typed_value(self, value):
        """Define o valor convertendo para string"""
        if self.value_type == 'json':
            self.value = json.dumps(value)
        else:
            self.value = str(value)
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def get_config(key, default=None):
        """Obtém um valor de configuração"""
        config = SystemConfig.query.filter_by(key=key).first()
        if config:
            return config.get_typed_value()
        return default
    
    @staticmethod
    def set_config(key, value, value_type='string', description=None, category='general', is_sensitive=False, updated_by=None):
        """Define um valor de configuração"""
        config = SystemConfig.query.filter_by(key=key).first()
        if config:
            config.set_typed_value(value)
            config.updated_by = updated_by
        else:
            config = SystemConfig(
                key=key,
                value_type=value_type,
                description=description,
                category=category,
                is_sensitive=is_sensitive,
                updated_by=updated_by
            )
            config.set_typed_value(value)
            db.session.add(config)
        
        db.session.commit()
        return config
    
    @staticmethod
    def initialize_default_configs():
        """Inicializa configurações padrão do sistema"""
        defaults = [
            {
                'key': 'daily_check_time',
                'value': '08:00',
                'value_type': 'string',
                'description': 'Horário diário para execução das consultas (formato HH:MM)',
                'category': 'scheduling'
            },
            {
                'key': 'max_concurrent_queries',
                'value': '5',
                'value_type': 'integer',
                'description': 'Número máximo de consultas simultâneas',
                'category': 'performance'
            },
            {
                'key': 'query_timeout_seconds',
                'value': '30',
                'value_type': 'integer',
                'description': 'Timeout para consultas à API em segundos',
                'category': 'performance'
            },
            {
                'key': 'retry_failed_queries',
                'value': 'true',
                'value_type': 'boolean',
                'description': 'Se deve tentar novamente consultas que falharam',
                'category': 'reliability'
            },
            {
                'key': 'max_retry_attempts',
                'value': '3',
                'value_type': 'integer',
                'description': 'Número máximo de tentativas para consultas que falharam',
                'category': 'reliability'
            },
            {
                'key': 'notification_email_enabled',
                'value': 'false',
                'value_type': 'boolean',
                'description': 'Se deve enviar notificações por email',
                'category': 'notifications'
            },
            {
                'key': 'notification_email_recipients',
                'value': '[]',
                'value_type': 'json',
                'description': 'Lista de emails para receber notificações',
                'category': 'notifications'
            },
            {
                'key': 'cache_results_hours',
                'value': '6',
                'value_type': 'integer',
                'description': 'Número de horas para manter resultados em cache',
                'category': 'performance'
            },
            {
                'key': 'api_base_url',
                'value': 'https://mob.processotelematico.giustizia.it/proxy/index_mobile',
                'value_type': 'string',
                'description': 'URL base da API da Giustizia Civile',
                'category': 'api'
            },
            {
                'key': 'enable_detailed_logging',
                'value': 'true',
                'value_type': 'boolean',
                'description': 'Se deve habilitar logging detalhado',
                'category': 'system'
            }
        ]
        
        for config_data in defaults:
            existing = SystemConfig.query.filter_by(key=config_data['key']).first()
            if not existing:
                SystemConfig.set_config(**config_data)

