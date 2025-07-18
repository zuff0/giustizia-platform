from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.credential import Credential
from src.models.user import db
from src.services.giustizia_api import GiustiziaAPIService

credentials_bp = Blueprint('credentials', __name__)
giustizia_service = GiustiziaAPIService()

@credentials_bp.route('/credentials', methods=['GET'])
def get_credentials():
    """Lista todas as credenciais"""
    try:
        include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        
        query = Credential.query
        
        if active_only:
            query = query.filter(Credential.is_active == True)
        
        credentials = query.order_by(Credential.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'credentials': [cred.to_dict(include_sensitive=include_sensitive) for cred in credentials]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials', methods=['POST'])
def create_credential():
    """Cria uma nova credencial"""
    try:
        data = request.get_json()
        
        # Validação de campos obrigatórios
        required_fields = ['name', 'uuid', 'token', 'device_name', 'device_width', 'device_height']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }), 400
        
        # Verifica se UUID já existe
        existing = Credential.query.filter_by(uuid=data['uuid']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': 'UUID já existe no sistema'
            }), 400
        
        # Cria nova credencial
        credential = Credential(
            name=data['name'],
            uuid=data['uuid'],
            token=data['token'],
            device_name=data['device_name'],
            device_width=data['device_width'],
            device_height=data['device_height'],
            platform=data.get('platform', 'iOS 12.1'),
            version=data.get('version', '1.1.13'),
            max_requests_per_minute=data.get('max_requests_per_minute', 60)
        )
        
        db.session.add(credential)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'credential': credential.to_dict(),
            'message': 'Credencial criada com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/<int:credential_id>', methods=['GET'])
def get_credential(credential_id):
    """Obtém detalhes de uma credencial específica"""
    try:
        credential = Credential.query.get_or_404(credential_id)
        include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
        
        return jsonify({
            'success': True,
            'credential': credential.to_dict(include_sensitive=include_sensitive)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/<int:credential_id>', methods=['PUT'])
def update_credential(credential_id):
    """Atualiza uma credencial"""
    try:
        credential = Credential.query.get_or_404(credential_id)
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = [
            'name', 'token', 'device_name', 'device_width', 'device_height',
            'platform', 'version', 'max_requests_per_minute', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'max_requests_per_minute':
                    setattr(credential, field, int(data[field]))
                elif field == 'is_active':
                    setattr(credential, field, bool(data[field]))
                else:
                    setattr(credential, field, data[field])
        
        credential.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'credential': credential.to_dict(),
            'message': 'Credencial atualizada com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/<int:credential_id>', methods=['DELETE'])
def delete_credential(credential_id):
    """Remove uma credencial"""
    try:
        credential = Credential.query.get_or_404(credential_id)
        
        # Marca como inativa ao invés de deletar
        credential.is_active = False
        credential.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Credencial desativada com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/<int:credential_id>/test', methods=['POST'])
def test_credential(credential_id):
    """Testa uma credencial específica"""
    try:
        credential = Credential.query.get_or_404(credential_id)
        
        if not credential.is_active:
            return jsonify({
                'success': False,
                'error': 'Credencial inativa'
            }), 400
        
        # Testa a credencial
        success, message = giustizia_service.test_credential(credential)
        
        return jsonify({
            'success': success,
            'message': message,
            'credential_id': credential_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/available', methods=['GET'])
def get_available_credentials():
    """Lista credenciais disponíveis para uso"""
    try:
        credentials = Credential.query.filter_by(is_active=True).all()
        available_credentials = []
        
        for credential in credentials:
            if credential.can_make_request():
                cred_data = credential.to_dict()
                cred_data['available'] = True
                available_credentials.append(cred_data)
            else:
                cred_data = credential.to_dict()
                cred_data['available'] = False
                cred_data['reason'] = 'Rate limit atingido'
                available_credentials.append(cred_data)
        
        return jsonify({
            'success': True,
            'credentials': available_credentials,
            'available_count': len([c for c in available_credentials if c['available']])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/stats', methods=['GET'])
def get_credentials_stats():
    """Obtém estatísticas das credenciais"""
    try:
        total_credentials = Credential.query.count()
        active_credentials = Credential.query.filter_by(is_active=True).count()
        
        # Credenciais disponíveis agora
        available_now = 0
        credentials = Credential.query.filter_by(is_active=True).all()
        for credential in credentials:
            if credential.can_make_request():
                available_now += 1
        
        # Estatísticas de uso
        total_requests = db.session.query(
            db.func.sum(Credential.total_requests)
        ).scalar() or 0
        
        successful_requests = db.session.query(
            db.func.sum(Credential.successful_requests)
        ).scalar() or 0
        
        failed_requests = db.session.query(
            db.func.sum(Credential.failed_requests)
        ).scalar() or 0
        
        avg_response_time = db.session.query(
            db.func.avg(Credential.average_response_time)
        ).filter(Credential.average_response_time > 0).scalar() or 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_credentials': total_credentials,
                'active_credentials': active_credentials,
                'available_now': available_now,
                'total_requests': int(total_requests),
                'successful_requests': int(successful_requests),
                'failed_requests': int(failed_requests),
                'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
                'average_response_time': round(float(avg_response_time), 2)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@credentials_bp.route('/credentials/reset-limits', methods=['POST'])
def reset_rate_limits():
    """Reseta os limites de rate limiting de todas as credenciais"""
    try:
        credentials = Credential.query.filter_by(is_active=True).all()
        
        for credential in credentials:
            credential.requests_this_minute = 0
            credential.minute_window_start = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Limites resetados para {len(credentials)} credenciais'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

