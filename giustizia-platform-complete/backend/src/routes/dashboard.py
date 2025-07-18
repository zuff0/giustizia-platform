from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.client import Client
from src.models.credential import Credential
from src.models.query_history import QueryHistory
from src.models.notification import Notification
from src.models.system_config import SystemConfig
from src.models.user import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """Obtém dados gerais para o dashboard"""
    try:
        # Estatísticas básicas
        total_clients = Client.query.filter_by(is_active=True).count()
        total_credentials = Credential.query.filter_by(is_active=True).count()
        
        # Credenciais disponíveis agora
        available_credentials = 0
        credentials = Credential.query.filter_by(is_active=True).all()
        for credential in credentials:
            if credential.can_make_request():
                available_credentials += 1
        
        # Estatísticas das últimas 24 horas
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        queries_24h = QueryHistory.query.filter(
            QueryHistory.query_timestamp >= yesterday
        ).count()
        
        successful_queries_24h = QueryHistory.query.filter(
            QueryHistory.query_timestamp >= yesterday,
            QueryHistory.response_status == 'success'
        ).count()
        
        status_changes_24h = QueryHistory.query.filter(
            QueryHistory.query_timestamp >= yesterday,
            QueryHistory.status_changed == True
        ).count()
        
        # Notificações não lidas
        unread_notifications = Notification.query.filter_by(is_read=False).count()
        
        # Últimas mudanças de status
        recent_changes = db.session.query(QueryHistory, Client).join(Client).filter(
            QueryHistory.status_changed == True,
            QueryHistory.query_timestamp >= yesterday
        ).order_by(QueryHistory.query_timestamp.desc()).limit(10).all()
        
        recent_changes_data = []
        for query, client in recent_changes:
            recent_changes_data.append({
                'client_name': client.name,
                'process_number': client.process_number,
                'process_year': client.process_year,
                'previous_status': query.previous_status,
                'new_status': query.status_result,
                'timestamp': query.query_timestamp.isoformat()
            })
        
        # Distribuição de status
        status_distribution = db.session.query(
            Client.current_status,
            db.func.count(Client.id).label('count')
        ).filter(
            Client.is_active == True,
            Client.current_status.isnot(None)
        ).group_by(Client.current_status).all()
        
        return jsonify({
            'success': True,
            'overview': {
                'total_clients': total_clients,
                'total_credentials': total_credentials,
                'available_credentials': available_credentials,
                'queries_24h': queries_24h,
                'successful_queries_24h': successful_queries_24h,
                'success_rate_24h': (successful_queries_24h / queries_24h * 100) if queries_24h > 0 else 0,
                'status_changes_24h': status_changes_24h,
                'unread_notifications': unread_notifications,
                'recent_changes': recent_changes_data,
                'status_distribution': [
                    {'status': status or 'Sem status', 'count': count}
                    for status, count in status_distribution
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/activity', methods=['GET'])
def get_activity_data():
    """Obtém dados de atividade para gráficos"""
    try:
        days = request.args.get('days', 7, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Consultas por dia
        daily_queries = db.session.query(
            db.func.date(QueryHistory.query_timestamp).label('date'),
            db.func.count(QueryHistory.id).label('total'),
            db.func.sum(db.case([(QueryHistory.response_status == 'success', 1)], else_=0)).label('successful')
        ).filter(
            QueryHistory.query_timestamp >= start_date
        ).group_by(
            db.func.date(QueryHistory.query_timestamp)
        ).order_by('date').all()
        
        activity_data = []
        for query_data in daily_queries:
            activity_data.append({
                'date': query_data.date.isoformat(),
                'total_queries': int(query_data.total),
                'successful_queries': int(query_data.successful or 0),
                'failed_queries': int(query_data.total) - int(query_data.successful or 0)
            })
        
        # Performance por credencial
        credential_performance = db.session.query(
            Credential.name,
            Credential.total_requests,
            Credential.successful_requests,
            Credential.failed_requests,
            Credential.average_response_time
        ).filter(Credential.is_active == True).all()
        
        performance_data = []
        for cred in credential_performance:
            performance_data.append({
                'credential_name': cred.name,
                'total_requests': cred.total_requests,
                'successful_requests': cred.successful_requests,
                'failed_requests': cred.failed_requests,
                'success_rate': (cred.successful_requests / cred.total_requests * 100) if cred.total_requests > 0 else 0,
                'average_response_time': round(cred.average_response_time, 2)
            })
        
        return jsonify({
            'success': True,
            'activity': {
                'daily_queries': activity_data,
                'credential_performance': performance_data
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Lista notificações com filtros"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        notification_type = request.args.get('type', '')
        
        query = Notification.query
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        
        pagination = query.order_by(Notification.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        notifications = [notif.to_dict() for notif in pagination.items]
        
        return jsonify({
            'success': True,
            'notifications': notifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Marca uma notificação como lida"""
    try:
        notification = Notification.query.get_or_404(notification_id)
        notification.mark_as_read()
        
        return jsonify({
            'success': True,
            'message': 'Notificação marcada como lida'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    """Marca todas as notificações como lidas"""
    try:
        unread_notifications = Notification.query.filter_by(is_read=False).all()
        
        for notification in unread_notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{len(unread_notifications)} notificações marcadas como lidas'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/system/config', methods=['GET'])
def get_system_config():
    """Obtém configurações do sistema"""
    try:
        category = request.args.get('category', '')
        include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
        
        query = SystemConfig.query
        
        if category:
            query = query.filter(SystemConfig.category == category)
        
        configs = query.order_by(SystemConfig.category, SystemConfig.key).all()
        
        config_data = {}
        for config in configs:
            if config.category not in config_data:
                config_data[config.category] = {}
            
            config_dict = config.to_dict(include_sensitive=include_sensitive)
            config_data[config.category][config.key] = config_dict
        
        return jsonify({
            'success': True,
            'config': config_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/system/config', methods=['POST'])
def update_system_config():
    """Atualiza configurações do sistema"""
    try:
        data = request.get_json()
        
        updated_configs = []
        for key, value in data.items():
            config = SystemConfig.set_config(
                key=key,
                value=value,
                updated_by='api_user'  # Pode ser melhorado com autenticação
            )
            updated_configs.append(config.key)
        
        return jsonify({
            'success': True,
            'message': f'{len(updated_configs)} configurações atualizadas',
            'updated_keys': updated_configs
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/system/health', methods=['GET'])
def get_system_health():
    """Verifica a saúde do sistema"""
    try:
        health_data = {
            'database': 'ok',
            'credentials': 'ok',
            'api_connectivity': 'ok',
            'overall_status': 'healthy'
        }
        
        # Verifica banco de dados
        try:
            db.session.execute('SELECT 1')
        except Exception:
            health_data['database'] = 'error'
            health_data['overall_status'] = 'unhealthy'
        
        # Verifica credenciais disponíveis
        available_credentials = 0
        total_credentials = Credential.query.filter_by(is_active=True).count()
        
        if total_credentials == 0:
            health_data['credentials'] = 'warning'
            health_data['overall_status'] = 'degraded'
        else:
            credentials = Credential.query.filter_by(is_active=True).all()
            for credential in credentials:
                if credential.can_make_request():
                    available_credentials += 1
            
            if available_credentials == 0:
                health_data['credentials'] = 'error'
                health_data['overall_status'] = 'unhealthy'
            elif available_credentials < total_credentials * 0.5:
                health_data['credentials'] = 'warning'
                health_data['overall_status'] = 'degraded'
        
        health_data['available_credentials'] = available_credentials
        health_data['total_credentials'] = total_credentials
        
        return jsonify({
            'success': True,
            'health': health_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'health': {
                'overall_status': 'error'
            }
        }), 500

