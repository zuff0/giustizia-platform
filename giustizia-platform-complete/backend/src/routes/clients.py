from flask import Blueprint, request, jsonify, send_file
import os
from datetime import datetime
from src.models.client import Client
from src.models.query_history import QueryHistory
from src.models.notification import Notification
from src.models.user import db
from src.services.giustizia_api import GiustiziaAPIService

clients_bp = Blueprint('clients', __name__)
giustizia_service = GiustiziaAPIService()

@clients_bp.route('/clients', methods=['GET'])
def get_clients():
    """Lista todos os clientes com filtros opcionais"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search = request.args.get('search', '')
        status_filter = request.args.get('status', '')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        query = Client.query
        
        # Filtro por status ativo
        if active_only:
            query = query.filter(Client.is_active == True)
        
        # Filtro de busca
        if search:
            query = query.filter(
                db.or_(
                    Client.name.ilike(f'%{search}%'),
                    Client.process_number.ilike(f'%{search}%'),
                    Client.email.ilike(f'%{search}%')
                )
            )
        
        # Filtro por status
        if status_filter:
            query = query.filter(Client.current_status.ilike(f'%{status_filter}%'))
        
        # Ordenação
        query = query.order_by(Client.created_at.desc())
        
        # Paginação
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        clients = [client.to_dict() for client in pagination.items]
        
        return jsonify({
            'success': True,
            'clients': clients,
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

@clients_bp.route('/clients', methods=['POST'])
def create_client():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validação de campos obrigatórios
        required_fields = ['name', 'process_number', 'process_year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Campo obrigatório: {field}'
                }), 400
        
        # Verifica se já existe um cliente com o mesmo processo
        existing = Client.query.filter_by(
            process_number=data['process_number'],
            process_year=data['process_year']
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'error': 'Já existe um cliente com este número de processo e ano'
            }), 400
        
        # Cria novo cliente
        client = Client(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            document_number=data.get('document_number'),
            process_number=data['process_number'],
            process_year=int(data['process_year']),
            notes=data.get('notes')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'client': client.to_dict(),
            'message': 'Cliente criado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Obtém detalhes de um cliente específico"""
    try:
        client = Client.query.get_or_404(client_id)
        
        # Inclui histórico recente de consultas
        recent_queries = QueryHistory.query.filter_by(client_id=client_id)\
            .order_by(QueryHistory.query_timestamp.desc())\
            .limit(10).all()
        
        # Inclui notificações recentes
        recent_notifications = Notification.query.filter_by(client_id=client_id)\
            .order_by(Notification.created_at.desc())\
            .limit(5).all()
        
        client_data = client.to_dict()
        client_data['recent_queries'] = [query.to_dict() for query in recent_queries]
        client_data['recent_notifications'] = [notif.to_dict() for notif in recent_notifications]
        
        return jsonify({
            'success': True,
            'client': client_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Atualiza dados de um cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = [
            'name', 'email', 'phone', 'document_number', 
            'process_number', 'process_year', 'notes', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'process_year':
                    setattr(client, field, int(data[field]))
                else:
                    setattr(client, field, data[field])
        
        client.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'client': client.to_dict(),
            'message': 'Cliente atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Remove um cliente (soft delete)"""
    try:
        client = Client.query.get_or_404(client_id)
        
        # Soft delete - marca como inativo
        client.is_active = False
        client.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente removido com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/<int:client_id>/query', methods=['POST'])
def query_client_status(client_id):
    """Consulta o status atual de um cliente específico"""
    try:
        client = Client.query.get_or_404(client_id)
        
        if not client.is_active:
            return jsonify({
                'success': False,
                'error': 'Cliente inativo'
            }), 400
        
        # Faz a consulta
        success, result, raw_response = giustizia_service.query_process_status(client)
        
        if success:
            return jsonify({
                'success': True,
                'status': result,
                'message': 'Consulta realizada com sucesso',
                'client': client.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'error': result,
                'message': 'Falha na consulta'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/<int:client_id>/history', methods=['GET'])
def get_client_history(client_id):
    """Obtém histórico de consultas de um cliente"""
    try:
        client = Client.query.get_or_404(client_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = QueryHistory.query.filter_by(client_id=client_id)\
            .order_by(QueryHistory.query_timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        history = [query.to_dict() for query in pagination.items]
        
        return jsonify({
            'success': True,
            'history': history,
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

@clients_bp.route('/clients/bulk-query', methods=['POST'])
def bulk_query_clients():
    """Consulta múltiplos clientes em lote"""
    try:
        data = request.get_json()
        client_ids = data.get('client_ids', [])
        
        if not client_ids:
            return jsonify({
                'success': False,
                'error': 'Lista de IDs de clientes é obrigatória'
            }), 400
        
        # Limita o número de consultas simultâneas
        if len(client_ids) > 50:
            return jsonify({
                'success': False,
                'error': 'Máximo de 50 clientes por consulta em lote'
            }), 400
        
        results = giustizia_service.query_multiple_clients(client_ids)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f'Consulta em lote concluída para {len(client_ids)} clientes'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@clients_bp.route('/clients/stats', methods=['GET'])
def get_clients_stats():
    """Obtém estatísticas gerais dos clientes"""
    try:
        total_clients = Client.query.filter_by(is_active=True).count()
        clients_with_status = Client.query.filter(
            Client.is_active == True,
            Client.current_status.isnot(None)
        ).count()
        
        # Últimas consultas (últimas 24h)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_queries = QueryHistory.query.filter(
            QueryHistory.query_timestamp >= yesterday
        ).count()
        
        successful_queries = QueryHistory.query.filter(
            QueryHistory.query_timestamp >= yesterday,
            QueryHistory.response_status == 'success'
        ).count()
        
        # Status mais comuns
        status_counts = db.session.query(
            Client.current_status,
            db.func.count(Client.id).label('count')
        ).filter(
            Client.is_active == True,
            Client.current_status.isnot(None)
        ).group_by(Client.current_status).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_clients': total_clients,
                'clients_with_status': clients_with_status,
                'recent_queries_24h': recent_queries,
                'successful_queries_24h': successful_queries,
                'success_rate_24h': (successful_queries / recent_queries * 100) if recent_queries > 0 else 0,
                'status_distribution': [
                    {'status': status, 'count': count} 
                    for status, count in status_counts
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@clients_bp.route('/clients/bulk-import', methods=['POST'])
def bulk_import_clients():
    """Importa clientes em lote via CSV/Excel"""
    try:
        # Verifica se foi enviado um arquivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo foi enviado'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verifica extensão do arquivo
        allowed_extensions = {'.csv', '.xlsx', '.xls'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'error': 'Formato de arquivo não suportado. Use CSV ou Excel (.xlsx, .xls)'
            }), 400
        
        # Processa o arquivo
        import pandas as pd
        import io
        
        try:
            # Lê o arquivo baseado na extensão
            if file_ext == '.csv':
                # Tenta diferentes encodings para CSV
                content = file.read()
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(io.StringIO(content.decode(encoding)))
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Não foi possível decodificar o arquivo CSV. Verifique a codificação.'
                    }), 400
            else:
                # Excel
                df = pd.read_excel(file)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Erro ao ler arquivo: {str(e)}'
            }), 400
        
        # Valida colunas obrigatórias
        required_columns = ['nome', 'processo', 'ano']
        df_columns_lower = [col.lower().strip() for col in df.columns]
        
        # Mapeia nomes de colunas flexíveis
        column_mapping = {}
        for req_col in required_columns:
            found = False
            for i, col in enumerate(df_columns_lower):
                if req_col in col or col in req_col:
                    column_mapping[req_col] = df.columns[i]
                    found = True
                    break
            
            if not found:
                return jsonify({
                    'success': False,
                    'error': f'Coluna obrigatória não encontrada: {req_col}. Colunas disponíveis: {list(df.columns)}'
                }), 400
        
        # Mapeia colunas opcionais
        optional_mapping = {}
        optional_columns = ['email', 'telefone', 'documento', 'observacoes']
        for opt_col in optional_columns:
            for i, col in enumerate(df_columns_lower):
                if opt_col in col or col in opt_col:
                    optional_mapping[opt_col] = df.columns[i]
                    break
        
        # Processa os dados
        successful_imports = 0
        failed_imports = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Extrai dados obrigatórios
                name = str(row[column_mapping['nome']]).strip()
                process_number = str(row[column_mapping['processo']]).strip()
                process_year = int(row[column_mapping['ano']])
                
                # Valida dados obrigatórios
                if not name or name.lower() in ['nan', 'none', '']:
                    errors.append(f'Linha {index + 2}: Nome é obrigatório')
                    failed_imports += 1
                    continue
                
                if not process_number or process_number.lower() in ['nan', 'none', '']:
                    errors.append(f'Linha {index + 2}: Número do processo é obrigatório')
                    failed_imports += 1
                    continue
                
                if process_year < 1900 or process_year > 2030:
                    errors.append(f'Linha {index + 2}: Ano do processo inválido ({process_year})')
                    failed_imports += 1
                    continue
                
                # Verifica se já existe
                existing = Client.query.filter_by(
                    process_number=process_number,
                    process_year=process_year
                ).first()
                
                if existing:
                    errors.append(f'Linha {index + 2}: Cliente já existe (processo {process_number}/{process_year})')
                    failed_imports += 1
                    continue
                
                # Extrai dados opcionais
                email = None
                if 'email' in optional_mapping:
                    email_val = str(row[optional_mapping['email']]).strip()
                    if email_val and email_val.lower() not in ['nan', 'none', '']:
                        email = email_val
                
                phone = None
                if 'telefone' in optional_mapping:
                    phone_val = str(row[optional_mapping['telefone']]).strip()
                    if phone_val and phone_val.lower() not in ['nan', 'none', '']:
                        phone = phone_val
                
                document_number = None
                if 'documento' in optional_mapping:
                    doc_val = str(row[optional_mapping['documento']]).strip()
                    if doc_val and doc_val.lower() not in ['nan', 'none', '']:
                        document_number = doc_val
                
                notes = None
                if 'observacoes' in optional_mapping:
                    notes_val = str(row[optional_mapping['observacoes']]).strip()
                    if notes_val and notes_val.lower() not in ['nan', 'none', '']:
                        notes = notes_val
                
                # Cria o cliente
                client = Client(
                    name=name,
                    email=email,
                    phone=phone,
                    document_number=document_number,
                    process_number=process_number,
                    process_year=process_year,
                    notes=notes
                )
                
                db.session.add(client)
                successful_imports += 1
                
            except Exception as e:
                errors.append(f'Linha {index + 2}: {str(e)}')
                failed_imports += 1
                continue
        
        # Salva as alterações
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': f'Erro ao salvar no banco de dados: {str(e)}'
            }), 500
        
        # Cria notificação de importação
        if successful_imports > 0:
            Notification.create_system_alert(
                "Importação de Clientes Concluída",
                f"Importados {successful_imports} clientes com sucesso. {failed_imports} falharam.",
                "success" if failed_imports == 0 else "warning"
            )
        
        return jsonify({
            'success': True,
            'message': f'Importação concluída: {successful_imports} sucessos, {failed_imports} falhas',
            'stats': {
                'successful_imports': successful_imports,
                'failed_imports': failed_imports,
                'total_processed': successful_imports + failed_imports,
                'errors': errors[:10]  # Limita a 10 erros para não sobrecarregar
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@clients_bp.route('/clients/import-template', methods=['GET'])
def download_import_template():
    """Baixa template para importação de clientes"""
    try:
        import pandas as pd
        import io
        
        # Cria template com dados de exemplo
        template_data = {
            'Nome': [
                'João Silva',
                'Maria Santos',
                'Carlos Oliveira'
            ],
            'Processo': [
                '12345',
                '67890',
                '11111'
            ],
            'Ano': [
                2024,
                2024,
                2023
            ],
            'Email': [
                'joao.silva@email.com',
                'maria.santos@email.com',
                'carlos.oliveira@email.com'
            ],
            'Telefone': [
                '(11) 99999-9999',
                '(21) 88888-8888',
                '(31) 77777-7777'
            ],
            'Documento': [
                '123.456.789-00',
                '987.654.321-00',
                '456.789.123-00'
            ],
            'Observacoes': [
                'Cliente prioritário',
                'Processo urgente',
                'Acompanhar de perto'
            ]
        }
        
        df = pd.DataFrame(template_data)
        
        # Cria arquivo Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Clientes', index=False)
            
            # Adiciona instruções em uma segunda aba
            instructions = pd.DataFrame({
                'INSTRUÇÕES PARA IMPORTAÇÃO': [
                    '1. Preencha os dados dos clientes nas colunas correspondentes',
                    '2. Colunas obrigatórias: Nome, Processo, Ano',
                    '3. Colunas opcionais: Email, Telefone, Documento, Observacoes',
                    '4. Não altere os nomes das colunas',
                    '5. Salve o arquivo e faça o upload na plataforma',
                    '',
                    'FORMATOS ACEITOS:',
                    '• Excel (.xlsx, .xls)',
                    '• CSV (.csv)',
                    '',
                    'LIMITES:',
                    '• Máximo 1000 clientes por importação',
                    '• Arquivo máximo: 10MB'
                ]
            })
            instructions.to_excel(writer, sheet_name='Instruções', index=False)
        
        output.seek(0)
        
        from flask import send_file
        return send_file(
            io.BytesIO(output.read()),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='template_importacao_clientes.xlsx'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao gerar template: {str(e)}'
        }), 500

