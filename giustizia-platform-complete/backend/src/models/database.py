import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

class Database:
    """
    Classe para gerenciar o banco de dados SQLite
    """
    
    def __init__(self, db_path: str = "giustizia.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados e cria as tabelas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Tabela de clientes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        process_number TEXT NOT NULL,
                        process_year INTEGER NOT NULL,
                        email TEXT,
                        phone TEXT,
                        document TEXT,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(process_number, process_year)
                    )
                ''')
                
                # Tabela de credenciais
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS credentials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        uuid TEXT NOT NULL UNIQUE,
                        token TEXT NOT NULL,
                        device_type TEXT DEFAULT 'iPhone',
                        status TEXT DEFAULT 'active',
                        last_used TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de histórico de consultas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS query_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_id INTEGER,
                        process_number TEXT NOT NULL,
                        process_year INTEGER NOT NULL,
                        status TEXT,
                        success BOOLEAN NOT NULL,
                        error TEXT,
                        has_changes BOOLEAN DEFAULT FALSE,
                        raw_data TEXT,
                        query_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (client_id) REFERENCES clients (id)
                    )
                ''')
                
                # Tabela de notificações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        client_name TEXT,
                        process_number TEXT,
                        read BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de configurações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS settings (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Inserir configurações padrão
                default_settings = {
                    'email_notifications': 'true',
                    'daily_queries': 'true',
                    'notification_email': 'admin@empresa.com',
                    'query_time': '08:00',
                    'max_retries': '3',
                    'timeout_seconds': '30',
                    'batch_size': '10'
                }
                
                for key, value in default_settings.items():
                    cursor.execute('''
                        INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)
                    ''', (key, value))
                
                conn.commit()
                self.logger.info("Banco de dados inicializado com sucesso")
                
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        try:
            yield conn
        finally:
            conn.close()
    
    # MÉTODOS PARA CLIENTES
    
    def create_client(self, client_data: Dict) -> int:
        """Cria um novo cliente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO clients (name, process_number, process_year, email, phone, document, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    client_data['name'],
                    client_data['process_number'],
                    client_data['process_year'],
                    client_data.get('email'),
                    client_data.get('phone'),
                    client_data.get('document'),
                    client_data.get('notes')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("Processo já cadastrado")
        except Exception as e:
            self.logger.error(f"Erro ao criar cliente: {str(e)}")
            raise
    
    def get_all_clients(self) -> List[Dict]:
        """Retorna todos os clientes"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM clients ORDER BY name')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar clientes: {str(e)}")
            return []
    
    def get_client(self, client_id: int) -> Optional[Dict]:
        """Retorna um cliente específico"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Erro ao buscar cliente: {str(e)}")
            return None
    
    def update_client(self, client_id: int, client_data: Dict) -> bool:
        """Atualiza um cliente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE clients 
                    SET name = ?, process_number = ?, process_year = ?, 
                        email = ?, phone = ?, document = ?, notes = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    client_data['name'],
                    client_data['process_number'],
                    client_data['process_year'],
                    client_data.get('email'),
                    client_data.get('phone'),
                    client_data.get('document'),
                    client_data.get('notes'),
                    client_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao atualizar cliente: {str(e)}")
            return False
    
    def delete_client(self, client_id: int) -> bool:
        """Exclui um cliente"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao excluir cliente: {str(e)}")
            return False
    
    def bulk_import_clients(self, clients_data: List[Dict]) -> Dict:
        """Importa múltiplos clientes"""
        success_count = 0
        error_count = 0
        errors = []
        
        for client_data in clients_data:
            try:
                self.create_client(client_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Linha {success_count + error_count}: {str(e)}")
        
        return {
            'success': success_count,
            'errors': error_count,
            'error_details': errors
        }
    
    # MÉTODOS PARA CREDENCIAIS
    
    def create_credential(self, credential_data: Dict) -> int:
        """Cria uma nova credencial"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO credentials (name, uuid, token, device_type)
                    VALUES (?, ?, ?, ?)
                ''', (
                    credential_data['name'],
                    credential_data['uuid'],
                    credential_data['token'],
                    credential_data.get('device_type', 'iPhone')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError("UUID já cadastrado")
        except Exception as e:
            self.logger.error(f"Erro ao criar credencial: {str(e)}")
            raise
    
    def get_all_credentials(self) -> List[Dict]:
        """Retorna todas as credenciais"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM credentials ORDER BY name')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar credenciais: {str(e)}")
            return []
    
    def get_active_credentials(self) -> List[Dict]:
        """Retorna apenas credenciais ativas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM credentials WHERE status = "active" ORDER BY name')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar credenciais ativas: {str(e)}")
            return []
    
    def update_credential(self, credential_id: int, credential_data: Dict) -> bool:
        """Atualiza uma credencial"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE credentials 
                    SET name = ?, uuid = ?, token = ?, device_type = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    credential_data['name'],
                    credential_data['uuid'],
                    credential_data['token'],
                    credential_data.get('device_type', 'iPhone'),
                    credential_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao atualizar credencial: {str(e)}")
            return False
    
    def delete_credential(self, credential_id: int) -> bool:
        """Exclui uma credencial"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao excluir credencial: {str(e)}")
            return False
    
    def update_credential_last_used(self, credential_id: int):
        """Atualiza o último uso de uma credencial"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE credentials 
                    SET last_used = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (credential_id,))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Erro ao atualizar último uso: {str(e)}")
    
    # MÉTODOS PARA HISTÓRICO DE CONSULTAS
    
    def save_query_history(self, query_data: Dict):
        """Salva resultado de consulta no histórico"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO query_history 
                    (client_id, process_number, process_year, status, success, error, has_changes, raw_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    query_data.get('client_id'),
                    query_data['process_number'],
                    query_data['process_year'],
                    query_data.get('status'),
                    query_data['success'],
                    query_data.get('error'),
                    query_data.get('has_changes', False),
                    json.dumps(query_data.get('raw_data')) if query_data.get('raw_data') else None
                ))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {str(e)}")
    
    def get_query_history(self, client_id: int = None, limit: int = 100) -> List[Dict]:
        """Retorna histórico de consultas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if client_id:
                    cursor.execute('''
                        SELECT * FROM query_history 
                        WHERE client_id = ? 
                        ORDER BY query_timestamp DESC 
                        LIMIT ?
                    ''', (client_id, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM query_history 
                        ORDER BY query_timestamp DESC 
                        LIMIT ?
                    ''', (limit,))
                
                results = []
                for row in cursor.fetchall():
                    result = dict(row)
                    if result['raw_data']:
                        try:
                            result['raw_data'] = json.loads(result['raw_data'])
                        except:
                            pass
                    results.append(result)
                
                return results
        except Exception as e:
            self.logger.error(f"Erro ao buscar histórico: {str(e)}")
            return []
    
    # MÉTODOS PARA NOTIFICAÇÕES
    
    def create_notification(self, notification_data: Dict) -> int:
        """Cria uma nova notificação"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notifications (type, title, message, client_name, process_number, read)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    notification_data['type'],
                    notification_data['title'],
                    notification_data['message'],
                    notification_data.get('client_name'),
                    notification_data.get('process_number'),
                    notification_data.get('read', False)
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"Erro ao criar notificação: {str(e)}")
            raise
    
    def get_all_notifications(self) -> List[Dict]:
        """Retorna todas as notificações"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM notifications ORDER BY created_at DESC')
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar notificações: {str(e)}")
            return []
    
    def mark_notification_read(self, notification_id: int) -> bool:
        """Marca notificação como lida"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE notifications SET read = TRUE WHERE id = ?', (notification_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao marcar notificação: {str(e)}")
            return False
    
    def delete_notification(self, notification_id: int) -> bool:
        """Exclui uma notificação"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM notifications WHERE id = ?', (notification_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Erro ao excluir notificação: {str(e)}")
            return False
    
    def clear_all_notifications(self) -> bool:
        """Limpa todas as notificações"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM notifications')
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Erro ao limpar notificações: {str(e)}")
            return False
    
    # MÉTODOS PARA CONFIGURAÇÕES
    
    def get_settings(self) -> Dict:
        """Retorna todas as configurações"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT key, value FROM settings')
                settings = {}
                for row in cursor.fetchall():
                    key, value = row
                    # Converter valores booleanos
                    if value.lower() in ('true', 'false'):
                        settings[key] = value.lower() == 'true'
                    # Converter valores numéricos
                    elif value.isdigit():
                        settings[key] = int(value)
                    else:
                        settings[key] = value
                return settings
        except Exception as e:
            self.logger.error(f"Erro ao buscar configurações: {str(e)}")
            return {}
    
    def update_settings(self, settings_data: Dict) -> bool:
        """Atualiza configurações"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for key, value in settings_data.items():
                    # Converter valores para string
                    if isinstance(value, bool):
                        value_str = 'true' if value else 'false'
                    else:
                        value_str = str(value)
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO settings (key, value, updated_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                    ''', (key, value_str))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"Erro ao atualizar configurações: {str(e)}")
            return False
    
    # MÉTODOS PARA ESTATÍSTICAS
    
    def get_dashboard_stats(self) -> Dict:
        """Retorna estatísticas para o dashboard"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total de clientes
                cursor.execute('SELECT COUNT(*) FROM clients')
                total_clients = cursor.fetchone()[0]
                
                # Consultas hoje
                cursor.execute('''
                    SELECT COUNT(*) FROM query_history 
                    WHERE DATE(query_timestamp) = DATE('now')
                ''')
                queries_today = cursor.fetchone()[0]
                
                # Mudanças detectadas
                cursor.execute('SELECT COUNT(*) FROM query_history WHERE has_changes = TRUE')
                changes_detected = cursor.fetchone()[0]
                
                # Notificações não lidas
                cursor.execute('SELECT COUNT(*) FROM notifications WHERE read = FALSE')
                unread_notifications = cursor.fetchone()[0]
                
                return {
                    'total_clients': total_clients,
                    'queries_today': queries_today,
                    'changes_detected': changes_detected,
                    'unread_notifications': unread_notifications
                }
        except Exception as e:
            self.logger.error(f"Erro ao buscar estatísticas: {str(e)}")
            return {
                'total_clients': 0,
                'queries_today': 0,
                'changes_detected': 0,
                'unread_notifications': 0
            }
    
    def get_recent_updates(self, limit: int = 10) -> List[Dict]:
        """Retorna atualizações recentes para o dashboard"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT 
                        qh.id,
                        c.name as client_name,
                        qh.process_number,
                        qh.process_year,
                        qh.status as status_change,
                        qh.query_timestamp as updated_at,
                        CASE 
                            WHEN qh.has_changes THEN 'alta'
                            WHEN qh.success THEN 'baixa'
                            ELSE 'media'
                        END as priority
                    FROM query_history qh
                    LEFT JOIN clients c ON qh.client_id = c.id
                    WHERE qh.success = TRUE
                    ORDER BY qh.query_timestamp DESC
                    LIMIT ?
                ''', (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Erro ao buscar atualizações recentes: {str(e)}")
            return []

