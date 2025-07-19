from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Importar serviços e modelos
from models.database import Database
from services.giustizia_api import GiustiziaAPI
from services.scheduler import QueryScheduler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)  # Permitir CORS para o frontend

# debbugging
@app.before_first_request
def before_first_request():
    logger.info("Aplicação Flask inicializada com sucesso!")
    logger.info(f"Variáveis de ambiente: PORT={os.environ.get('PORT')}")

# Inicializar serviços
db = Database()
api = GiustiziaAPI()
scheduler = QueryScheduler(db)

# Iniciar scheduler
scheduler.start()

# ROTAS DE HEALTH CHECK

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# ROTAS DE CLIENTES

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Retorna todos os clientes"""
    try:
        clients = db.get_all_clients()
        return jsonify(clients)
    except Exception as e:
        logger.error(f"Erro ao buscar clientes: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/clients', methods=['POST'])
def create_client():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'process_number', 'process_year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        client_id = db.create_client(data)
        return jsonify({'id': client_id, 'message': 'Cliente criado com sucesso'}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar cliente: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Atualiza um cliente"""
    try:
        data = request.get_json()
        
        if db.update_client(client_id, data):
            return jsonify({'message': 'Cliente atualizado com sucesso'})
        else:
            return jsonify({'error': 'Cliente não encontrado'}), 404
            
    except Exception as e:
        logger.error(f"Erro ao atualizar cliente: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Exclui um cliente"""
    try:
        if db.delete_client(client_id):
            return jsonify({'message': 'Cliente excluído com sucesso'})
        else:
            return jsonify({'error': 'Cliente não encontrado'}), 404
            
    except Exception as e:
        logger.error(f"Erro ao excluir cliente: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/clients/bulk-import', methods=['POST'])
def bulk_import_clients():
    """Importa clientes em lote via CSV/Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Processar arquivo
        import pandas as pd
        import io
        
        # Ler arquivo
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        else:
            df = pd.read_excel(file)
        
        # Mapear colunas
        column_mapping = {
            'nome': 'name',
            'name': 'name',
            'processo': 'process_number',
            'process_number': 'process_number',
            'numero_processo': 'process_number',
            'ano': 'process_year',
            'process_year': 'process_year',
            'email': 'email',
            'telefone': 'phone',
            'phone': 'phone',
            'documento': 'document',
            'document': 'document',
            'observacoes': 'notes',
            'notes': 'notes',
            'observações': 'notes'
        }
        
        # Renomear colunas
        df.columns = df.columns.str.lower()
        df = df.rename(columns=column_mapping)
        
        # Converter para lista de dicionários
        clients_data = []
        for _, row in df.iterrows():
            client_data = {
                'name': str(row.get('name', '')).strip(),
                'process_number': str(row.get('process_number', '')).strip(),
                'process_year': int(row.get('process_year', 0)) if pd.notna(row.get('process_year')) else 0,
                'email': str(row.get('email', '')).strip() if pd.notna(row.get('email')) else None,
                'phone': str(row.get('phone', '')).strip() if pd.notna(row.get('phone')) else None,
                'document': str(row.get('document', '')).strip() if pd.notna(row.get('document')) else None,
                'notes': str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None
            }
            
            # Validar dados obrigatórios
            if client_data['name'] and client_data['process_number'] and client_data['process_year']:
                clients_data.append(client_data)
        
        # Importar clientes
        result = db.bulk_import_clients(clients_data)
        
        return jsonify({
            'message': f'Importação concluída: {result["success"]} sucessos, {result["errors"]} erros',
            'success': result['success'],
            'errors': result['errors'],
            'error_details': result['error_details']
        })
        
    except Exception as e:
        logger.error(f"Erro na importação em lote: {str(e)}")
        return jsonify({'error': f'Erro na importação: {str(e)}'}), 500

# ROTAS DE CREDENCIAIS

@app.route('/api/credentials', methods=['GET'])
def get_credentials():
    """Retorna todas as credenciais"""
    try:
        credentials = db.get_all_credentials()
        # Mascarar tokens por segurança
        for cred in credentials:
            if cred.get('token'):
                cred['token'] = cred['token'][:20] + '...' if len(cred['token']) > 20 else cred['token']
        return jsonify(credentials)
    except Exception as e:
        logger.error(f"Erro ao buscar credenciais: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/credentials', methods=['POST'])
def create_credential():
    """Cria uma nova credencial"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'uuid', 'token']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        credential_id = db.create_credential(data)
        return jsonify({'id': credential_id, 'message': 'Credencial criada com sucesso'}), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar credencial: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/credentials/<int:credential_id>', methods=['PUT'])
def update_credential(credential_id):
    """Atualiza uma credencial"""
    try:
        data = request.get_json()
        
        if db.update_credential(credential_id, data):
            return jsonify({'message': 'Credencial atualizada com sucesso'})
        else:
            return jsonify({'error': 'Credencial não encontrada'}), 404
            
    except Exception as e:
        logger.error(f"Erro ao atualizar credencial: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/credentials/<int:credential_id>', methods=['DELETE'])
def delete_credential(credential_id):
    """Exclui uma credencial"""
    try:
        if db.delete_credential(credential_id):
            return jsonify({'message': 'Credencial excluída com sucesso'})
        else:
            return jsonify({'error': 'Credencial não encontrada'}), 404
            
    except Exception as e:
        logger.error(f"Erro ao excluir credencial: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/credentials/<int:credential_id>/test', methods=['POST'])
def test_credential(credential_id):
    """Testa uma credencial"""
    try:
        # Buscar credencial
        credentials = db.get_all_credentials()
        credential = next((c for c in credentials if c['id'] == credential_id), None)
        
        if not credential:
            return jsonify({'error': 'Credencial não encontrada'}), 404
        
        # Testar credencial
        result = api.test_credentials(credential['uuid'], credential['token'])
        
        # Atualizar último uso se sucesso
        if result['success']:
            db.update_credential_last_used(credential_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro ao testar credencial: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ROTAS DE NOTIFICAÇÕES

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Retorna todas as notificações"""
    try:
        notifications = db.get_all_notifications()
        return jsonify(notifications)
    except Exception as e:
        logger.error(f"Erro ao buscar notificações: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    """Marca notificação como lida"""
    try:
        if db.mark_notification_read(notification_id):
            return jsonify({'message': 'Notificação marcada como lida'})
        else:
            return jsonify({'error': 'Notificação não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao marcar notificação: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Exclui uma notificação"""
    try:
        if db.delete_notification(notification_id):
            return jsonify({'message': 'Notificação excluída'})
        else:
            return jsonify({'error': 'Notificação não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao excluir notificação: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/notifications/clear', methods=['DELETE'])
def clear_notifications():
    """Limpa todas as notificações"""
    try:
        db.clear_all_notifications()
        return jsonify({'message': 'Todas as notificações foram removidas'})
    except Exception as e:
        logger.error(f"Erro ao limpar notificações: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ROTAS DE CONFIGURAÇÕES

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Retorna configurações do sistema"""
    try:
        settings = db.get_settings()
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Erro ao buscar configurações: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Atualiza configurações do sistema"""
    try:
        data = request.get_json()
        
        if db.update_settings(data):
            # Atualizar agendamento se necessário
            if 'query_time' in data:
                scheduler.update_schedule(data['query_time'])
            
            return jsonify({'message': 'Configurações atualizadas com sucesso'})
        else:
            return jsonify({'error': 'Erro ao atualizar configurações'}), 500
            
    except Exception as e:
        logger.error(f"Erro ao atualizar configurações: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ROTAS DE CONSULTAS

@app.route('/api/manual-query', methods=['POST'])
def manual_query():
    """Executa consulta manual"""
    try:
        data = request.get_json() or {}
        client_ids = data.get('client_ids')  # Lista de IDs ou None para todos
        
        result = scheduler.run_manual_query(client_ids)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Erro na consulta manual: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/query-history', methods=['GET'])
def get_query_history():
    """Retorna histórico de consultas"""
    try:
        client_id = request.args.get('client_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        
        history = db.get_query_history(client_id, limit)
        return jsonify(history)
        
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ROTAS DO DASHBOARD

@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Retorna estatísticas do dashboard"""
    try:
        stats = db.get_dashboard_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/recent-updates', methods=['GET'])
def get_recent_updates():
    """Retorna atualizações recentes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        updates = db.get_recent_updates(limit)
        return jsonify(updates)
    except Exception as e:
        logger.error(f"Erro ao buscar atualizações: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# ROTAS DE TESTE

@app.route('/api/test-email', methods=['POST'])
def test_email():
    """Testa envio de e-mail"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'E-mail é obrigatório'}), 400
        
        # Aqui você implementaria o envio real de e-mail
        # Por enquanto, apenas simular sucesso
        logger.info(f"Teste de e-mail para: {email}")
        
        return jsonify({'message': f'E-mail de teste enviado para {email}'})
        
    except Exception as e:
        logger.error(f"Erro no teste de e-mail: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """Retorna status do scheduler"""
    try:
        status = scheduler.get_scheduler_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Erro ao buscar status do scheduler: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# TRATAMENTO DE ERROS

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

# INICIALIZAÇÃO

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

