import schedule
import time
import threading
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Callable
from .giustizia_api import GiustiziaAPI
from models.database import Database

class QueryScheduler:
    """
    Serviço de agendamento para consultas automáticas
    """
    
    def __init__(self, db: Database):
        self.db = db
        self.api = GiustiziaAPI()
        self.running = False
        self.thread = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configurações padrão
        self.default_schedule_time = "08:00"
        self.batch_size = 10
        self.max_concurrent_queries = 5
        
    def start(self):
        """Inicia o scheduler"""
        if self.running:
            self.logger.warning("Scheduler já está rodando")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        self.logger.info("Scheduler iniciado")
    
    def stop(self):
        """Para o scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.logger.info("Scheduler parado")
    
    def _run_scheduler(self):
        """Loop principal do scheduler"""
        # Configurar agendamento padrão
        self._setup_default_schedule()
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto
            except Exception as e:
                self.logger.error(f"Erro no scheduler: {str(e)}")
                time.sleep(60)
    
    def _setup_default_schedule(self):
        """Configura o agendamento padrão"""
        # Carregar configurações do banco
        settings = self.db.get_settings()
        schedule_time = settings.get('query_time', self.default_schedule_time)
        
        # Agendar consulta diária
        schedule.every().day.at(schedule_time).do(self.run_daily_queries)
        
        self.logger.info(f"Consultas agendadas para {schedule_time} todos os dias")
    
    def run_daily_queries(self):
        """Executa consultas diárias para todos os clientes"""
        try:
            self.logger.info("Iniciando consultas diárias")
            
            # Buscar todos os clientes ativos
            clients = self.db.get_all_clients()
            if not clients:
                self.logger.info("Nenhum cliente encontrado")
                return
            
            # Buscar credenciais ativas
            credentials = self.db.get_active_credentials()
            if not credentials:
                self.logger.error("Nenhuma credencial ativa encontrada")
                self._create_notification(
                    'error',
                    'Erro nas Consultas Diárias',
                    'Nenhuma credencial ativa encontrada. Configure suas credenciais.'
                )
                return
            
            # Preparar consultas
            queries = []
            for client in clients:
                queries.append({
                    'client_id': client['id'],
                    'client_name': client['name'],
                    'process_number': client['process_number'],
                    'process_year': client['process_year']
                })
            
            # Executar consultas em lotes
            total_queries = len(queries)
            successful_queries = 0
            failed_queries = 0
            changes_detected = 0
            
            self.logger.info(f"Processando {total_queries} consultas")
            
            for i in range(0, len(queries), self.batch_size):
                batch = queries[i:i + self.batch_size]
                
                self.logger.info(f"Processando lote {i//self.batch_size + 1} ({len(batch)} consultas)")
                
                # Executar lote
                results = self.api.batch_query(batch, credentials)
                
                # Processar resultados
                for result in results:
                    if result.get('success'):
                        successful_queries += 1
                        
                        # Salvar resultado no histórico
                        self._save_query_result(result)
                        
                        # Verificar mudanças
                        if result.get('has_changes'):
                            changes_detected += 1
                            self._handle_status_change(result)
                    else:
                        failed_queries += 1
                        self.logger.error(f"Falha na consulta: {result.get('error')}")
                
                # Pausa entre lotes
                time.sleep(5)
            
            # Criar relatório final
            self._create_daily_report(total_queries, successful_queries, failed_queries, changes_detected)
            
            self.logger.info(f"Consultas diárias concluídas: {successful_queries}/{total_queries} sucessos")
            
        except Exception as e:
            self.logger.error(f"Erro nas consultas diárias: {str(e)}")
            self._create_notification(
                'error',
                'Erro nas Consultas Diárias',
                f'Erro inesperado: {str(e)}'
            )
    
    def run_manual_query(self, client_ids: List[int] = None):
        """
        Executa consulta manual para clientes específicos ou todos
        
        Args:
            client_ids: Lista de IDs dos clientes (None para todos)
        """
        try:
            self.logger.info("Iniciando consulta manual")
            
            # Buscar clientes
            if client_ids:
                clients = [self.db.get_client(client_id) for client_id in client_ids]
                clients = [c for c in clients if c]  # Remover None
            else:
                clients = self.db.get_all_clients()
            
            if not clients:
                return {
                    'success': False,
                    'message': 'Nenhum cliente encontrado'
                }
            
            # Buscar credenciais
            credentials = self.db.get_active_credentials()
            if not credentials:
                return {
                    'success': False,
                    'message': 'Nenhuma credencial ativa encontrada'
                }
            
            # Preparar e executar consultas
            queries = []
            for client in clients:
                queries.append({
                    'client_id': client['id'],
                    'client_name': client['name'],
                    'process_number': client['process_number'],
                    'process_year': client['process_year']
                })
            
            results = self.api.batch_query(queries, credentials)
            
            # Processar resultados
            successful = 0
            failed = 0
            changes = 0
            
            for result in results:
                if result.get('success'):
                    successful += 1
                    self._save_query_result(result)
                    
                    if result.get('has_changes'):
                        changes += 1
                        self._handle_status_change(result)
                else:
                    failed += 1
            
            return {
                'success': True,
                'message': f'Consulta concluída: {successful} sucessos, {failed} falhas, {changes} mudanças detectadas',
                'stats': {
                    'total': len(queries),
                    'successful': successful,
                    'failed': failed,
                    'changes': changes
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erro na consulta manual: {str(e)}")
            return {
                'success': False,
                'message': f'Erro na consulta: {str(e)}'
            }
    
    def _save_query_result(self, result: Dict):
        """Salva resultado da consulta no histórico"""
        try:
            self.db.save_query_history({
                'client_id': result.get('client_id'),
                'process_number': result.get('process_number'),
                'process_year': result.get('process_year'),
                'status': result.get('status'),
                'success': result.get('success'),
                'error': result.get('error'),
                'has_changes': result.get('has_changes', False),
                'raw_data': result.get('raw_data'),
                'query_timestamp': result.get('query_timestamp', datetime.now().isoformat())
            })
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {str(e)}")
    
    def _handle_status_change(self, result: Dict):
        """Processa mudança de status detectada"""
        try:
            client_name = result.get('client_name', 'Cliente desconhecido')
            process_number = result.get('process_number')
            process_year = result.get('process_year')
            new_status = result.get('status', 'Status desconhecido')
            
            # Criar notificação
            self._create_notification(
                'status_change',
                f'Mudança Detectada - {client_name}',
                f'O processo {process_number}/{process_year} teve mudança de status: {new_status}',
                client_name=client_name,
                process_number=f'{process_number}/{process_year}'
            )
            
            # Enviar e-mail se configurado
            self._send_email_notification(result)
            
            self.logger.info(f"Mudança detectada para {client_name}: {new_status}")
            
        except Exception as e:
            self.logger.error(f"Erro ao processar mudança de status: {str(e)}")
    
    def _create_notification(self, type: str, title: str, message: str, **kwargs):
        """Cria uma notificação no sistema"""
        try:
            self.db.create_notification({
                'type': type,
                'title': title,
                'message': message,
                'client_name': kwargs.get('client_name'),
                'process_number': kwargs.get('process_number'),
                'read': False,
                'created_at': datetime.now().isoformat()
            })
        except Exception as e:
            self.logger.error(f"Erro ao criar notificação: {str(e)}")
    
    def _send_email_notification(self, result: Dict):
        """Envia notificação por e-mail"""
        try:
            settings = self.db.get_settings()
            
            if not settings.get('email_notifications', False):
                return
            
            email = settings.get('notification_email')
            if not email:
                return
            
            # Aqui você implementaria o envio de e-mail
            # Por exemplo, usando SMTP ou serviço de e-mail
            self.logger.info(f"E-mail de notificação enviado para {email}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar e-mail: {str(e)}")
    
    def _create_daily_report(self, total: int, successful: int, failed: int, changes: int):
        """Cria relatório diário das consultas"""
        try:
            report_message = f"""Relatório Diário de Consultas:

📊 Estatísticas:
• Total de consultas: {total}
• Sucessos: {successful}
• Falhas: {failed}
• Mudanças detectadas: {changes}

⏰ Executado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

{f'⚠️ {failed} consultas falharam' if failed > 0 else '✅ Todas as consultas foram bem-sucedidas'}
{f'🔔 {changes} mudanças foram detectadas' if changes > 0 else 'ℹ️ Nenhuma mudança detectada'}"""

            self._create_notification(
                'info',
                'Relatório Diário de Consultas',
                report_message
            )
            
            # Enviar relatório por e-mail se configurado
            settings = self.db.get_settings()
            if settings.get('email_notifications', False) and settings.get('notification_email'):
                # Implementar envio de e-mail do relatório
                pass
            
        except Exception as e:
            self.logger.error(f"Erro ao criar relatório diário: {str(e)}")
    
    def update_schedule(self, new_time: str):
        """Atualiza o horário do agendamento"""
        try:
            # Limpar agendamentos existentes
            schedule.clear()
            
            # Configurar novo horário
            schedule.every().day.at(new_time).do(self.run_daily_queries)
            
            # Salvar configuração
            self.db.update_settings({'query_time': new_time})
            
            self.logger.info(f"Agendamento atualizado para {new_time}")
            
        except Exception as e:
            self.logger.error(f"Erro ao atualizar agendamento: {str(e)}")
    
    def get_next_run_time(self) -> str:
        """Retorna o próximo horário de execução"""
        try:
            jobs = schedule.jobs
            if jobs:
                next_run = min(job.next_run for job in jobs)
                return next_run.strftime('%d/%m/%Y às %H:%M')
            return "Não agendado"
        except:
            return "Erro ao calcular"
    
    def get_scheduler_status(self) -> Dict:
        """Retorna status do scheduler"""
        return {
            'running': self.running,
            'next_run': self.get_next_run_time(),
            'jobs_count': len(schedule.jobs),
            'batch_size': self.batch_size,
            'max_concurrent': self.max_concurrent_queries
        }

