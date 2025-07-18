#!/usr/bin/env python3
"""
Script para inicializar o banco de dados da plataforma Giustizia Civile
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app, db
from src.models.user import User
from src.models.client import Client
from src.models.query_history import QueryHistory
from src.models.credential import Credential
from src.models.notification import Notification
from src.models.system_config import SystemConfig

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    with app.app_context():
        print("Criando tabelas do banco de dados...")
        
        # Remove todas as tabelas existentes
        db.drop_all()
        
        # Cria todas as tabelas
        db.create_all()
        
        print("Tabelas criadas com sucesso!")
        
        # Adiciona configurações padrão do sistema
        print("Adicionando configurações padrão...")
        
        configs = [
            SystemConfig(key='max_queries_per_minute', value='60'),
            SystemConfig(key='query_timeout_seconds', value='30'),
            SystemConfig(key='retry_attempts', value='3'),
            SystemConfig(key='email_notifications_enabled', value='true'),
            SystemConfig(key='daily_query_time', value='08:00'),
            SystemConfig(key='notification_email', value='admin@empresa.com')
        ]
        
        for config in configs:
            db.session.add(config)
        
        # Adiciona alguns clientes de exemplo
        print("Adicionando dados de exemplo...")
        
        example_clients = [
            Client(
                name='João Silva',
                process_number='12345',
                process_year='2024',
                email='joao.silva@email.com',
                phone='(11) 99999-1111',
                current_status='Em Análise',
                notes='Cliente VIP - prioridade alta'
            ),
            Client(
                name='Maria Santos',
                process_number='67890',
                process_year='2024',
                email='maria.santos@email.com',
                phone='(11) 99999-2222',
                current_status='Pendente',
                notes='Aguardando documentação adicional'
            ),
            Client(
                name='Carlos Oliveira',
                process_number='11111',
                process_year='2024',
                email='carlos.oliveira@email.com',
                phone='(11) 99999-3333',
                current_status='Deferido',
                notes='Processo aprovado - aguardando finalização'
            )
        ]
        
        for client in example_clients:
            db.session.add(client)
        
        # Adiciona credencial de exemplo
        example_credential = Credential(
            name='Credencial Principal',
            uuid='example-uuid-12345',
            token='example-token-encrypted',
            device_name='iPhone',
            device_width='375',
            device_height='812',
            platform='iOS 12.1',
            version='1.1.13',
            is_active=True
        )
        db.session.add(example_credential)
        
        # Adiciona algumas notificações de exemplo
        example_notifications = [
            Notification(
                notification_type='system_alert',
                title='Sistema Inicializado',
                message='Plataforma Giustizia Civile inicializada com sucesso',
                severity='info',
                is_read=False
            ),
            Notification(
                notification_type='system_alert',
                title='Banco de Dados Configurado',
                message='Todas as tabelas foram criadas e dados de exemplo adicionados',
                severity='success',
                is_read=False
            )
        ]
        
        for notification in example_notifications:
            db.session.add(notification)
        
        # Salva todas as mudanças
        db.session.commit()
        
        print("Dados de exemplo adicionados com sucesso!")
        print("\nResumo:")
        print(f"- Clientes: {Client.query.count()}")
        print(f"- Credenciais: {Credential.query.count()}")
        print(f"- Notificações: {Notification.query.count()}")
        print(f"- Configurações: {SystemConfig.query.count()}")
        
        print("\nBanco de dados inicializado com sucesso! 🎉")

if __name__ == '__main__':
    init_database()

