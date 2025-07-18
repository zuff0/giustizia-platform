from flask import Blueprint, request, jsonify
from src.services.scheduler import SchedulerService
from src.models.system_config import SystemConfig

scheduler_bp = Blueprint('scheduler', __name__)

# Instância global do scheduler (será inicializada no main.py)
scheduler_service = None

def init_scheduler(app):
    """Inicializa o serviço de scheduler"""
    global scheduler_service
    scheduler_service = SchedulerService(app)
    scheduler_service.start()
    return scheduler_service

@scheduler_bp.route('/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """Obtém status do scheduler"""
    try:
        if not scheduler_service:
            return jsonify({
                'success': False,
                'error': 'Scheduler não inicializado'
            }), 500
        
        next_run = scheduler_service.get_next_scheduled_run()
        daily_time = SystemConfig.get_config('daily_check_time', '08:00')
        
        return jsonify({
            'success': True,
            'status': {
                'running': scheduler_service.running,
                'daily_time': daily_time,
                'next_run': next_run
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scheduler_bp.route('/scheduler/run-manual', methods=['POST'])
def run_manual_query():
    """Executa consulta manual"""
    try:
        if not scheduler_service:
            return jsonify({
                'success': False,
                'error': 'Scheduler não inicializado'
            }), 500
        
        data = request.get_json() or {}
        client_ids = data.get('client_ids')
        
        result = scheduler_service.run_manual_query(client_ids)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scheduler_bp.route('/scheduler/update-time', methods=['POST'])
def update_schedule_time():
    """Atualiza horário das consultas diárias"""
    try:
        if not scheduler_service:
            return jsonify({
                'success': False,
                'error': 'Scheduler não inicializado'
            }), 500
        
        data = request.get_json()
        new_time = data.get('time')
        
        if not new_time:
            return jsonify({
                'success': False,
                'error': 'Horário é obrigatório'
            }), 400
        
        # Valida formato do horário (HH:MM)
        try:
            hour, minute = new_time.split(':')
            hour = int(hour)
            minute = int(minute)
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError("Horário inválido")
                
        except (ValueError, IndexError):
            return jsonify({
                'success': False,
                'error': 'Formato de horário inválido. Use HH:MM'
            }), 400
        
        success = scheduler_service.update_schedule(new_time)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Horário atualizado para {new_time}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Falha ao atualizar horário'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scheduler_bp.route('/scheduler/start', methods=['POST'])
def start_scheduler():
    """Inicia o scheduler"""
    try:
        if not scheduler_service:
            return jsonify({
                'success': False,
                'error': 'Scheduler não inicializado'
            }), 500
        
        if scheduler_service.running:
            return jsonify({
                'success': False,
                'error': 'Scheduler já está rodando'
            }), 400
        
        scheduler_service.start()
        
        return jsonify({
            'success': True,
            'message': 'Scheduler iniciado com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@scheduler_bp.route('/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """Para o scheduler"""
    try:
        if not scheduler_service:
            return jsonify({
                'success': False,
                'error': 'Scheduler não inicializado'
            }), 500
        
        if not scheduler_service.running:
            return jsonify({
                'success': False,
                'error': 'Scheduler não está rodando'
            }), 400
        
        scheduler_service.stop()
        
        return jsonify({
            'success': True,
            'message': 'Scheduler parado com sucesso'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

