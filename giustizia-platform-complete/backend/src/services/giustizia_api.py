import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class GiustiziaAPI:
    """
    Serviço para integração com a API oficial da Giustizia Civile
    """
    
    def __init__(self):
        self.base_url = "https://mob.processotelematico.giustizia.it/proxy/index_mobile"
        self.session = requests.Session()
        self.rate_limit_delay = 1.0  # 1 segundo entre requisições
        self.max_retries = 3
        self.timeout = 30
        
        # Headers padrão para simular o app móvel oficial
        self.default_headers = {
            'User-Agent': 'GiustiziaCivile/1.0 (iPhone; iOS 15.0; Scale/3.00)',
            'Accept': 'application/json',
            'Accept-Language': 'it-IT,it;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def query_process(self, process_number: str, process_year: str, uuid: str, token: str) -> Dict:
        """
        Consulta um processo específico na API da Giustizia Civile
        
        Args:
            process_number: Número do processo
            process_year: Ano do processo
            uuid: UUID da credencial
            token: Token de autenticação
            
        Returns:
            Dict com os dados do processo ou erro
        """
        try:
            # Preparar headers com credenciais
            headers = self.default_headers.copy()
            headers.update({
                'uuid': uuid,
                'token': token,
                'device-id': uuid,
                'authorization': f'Bearer {token}'
            })
            
            # Preparar payload da consulta
            payload = {
                'numero_processo': process_number,
                'anno_processo': process_year,
                'tipo_ricerca': 'numero_processo',
                'timestamp': int(time.time() * 1000)
            }
            
            self.logger.info(f"Consultando processo {process_number}/{process_year}")
            
            # Fazer requisição com retry
            for attempt in range(self.max_retries):
                try:
                    response = self.session.post(
                        self.base_url,
                        headers=headers,
                        json=payload,
                        timeout=self.timeout
                    )
                    
                    # Rate limiting
                    time.sleep(self.rate_limit_delay)
                    
                    if response.status_code == 200:
                        data = response.json()
                        return self._parse_process_response(data, process_number, process_year)
                    
                    elif response.status_code == 401:
                        return {
                            'success': False,
                            'error': 'Credenciais inválidas ou expiradas',
                            'status_code': 401
                        }
                    
                    elif response.status_code == 429:
                        # Rate limit exceeded
                        wait_time = (attempt + 1) * 60  # Esperar 1, 2, 3 minutos
                        self.logger.warning(f"Rate limit exceeded. Aguardando {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    else:
                        self.logger.warning(f"Tentativa {attempt + 1} falhou: {response.status_code}")
                        if attempt == self.max_retries - 1:
                            return {
                                'success': False,
                                'error': f'Erro HTTP {response.status_code}',
                                'status_code': response.status_code
                            }
                
                except requests.exceptions.Timeout:
                    self.logger.warning(f"Timeout na tentativa {attempt + 1}")
                    if attempt == self.max_retries - 1:
                        return {
                            'success': False,
                            'error': 'Timeout na consulta',
                            'status_code': 408
                        }
                
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Erro na requisição: {str(e)}")
                    if attempt == self.max_retries - 1:
                        return {
                            'success': False,
                            'error': f'Erro de conexão: {str(e)}',
                            'status_code': 500
                        }
                
                # Aguardar antes da próxima tentativa
                time.sleep((attempt + 1) * 2)
            
        except Exception as e:
            self.logger.error(f"Erro inesperado: {str(e)}")
            return {
                'success': False,
                'error': f'Erro inesperado: {str(e)}',
                'status_code': 500
            }
    
    def _parse_process_response(self, data: Dict, process_number: str, process_year: str) -> Dict:
        """
        Processa a resposta da API e extrai informações relevantes
        """
        try:
            if not data or 'risultati' not in data:
                return {
                    'success': False,
                    'error': 'Processo não encontrado',
                    'process_number': process_number,
                    'process_year': process_year
                }
            
            risultati = data.get('risultati', [])
            if not risultati:
                return {
                    'success': False,
                    'error': 'Nenhum resultado encontrado',
                    'process_number': process_number,
                    'process_year': process_year
                }
            
            # Pegar o primeiro resultado (mais relevante)
            processo = risultati[0]
            
            # Extrair informações principais
            result = {
                'success': True,
                'process_number': process_number,
                'process_year': process_year,
                'status': processo.get('stato', 'Desconhecido'),
                'tribunal': processo.get('tribunale', ''),
                'judge': processo.get('giudice', ''),
                'parties': processo.get('parti', []),
                'last_update': processo.get('ultimo_aggiornamento', ''),
                'next_hearing': processo.get('prossima_udienza', ''),
                'documents': processo.get('documenti', []),
                'raw_data': processo,
                'query_timestamp': datetime.now().isoformat()
            }
            
            # Detectar mudanças significativas
            result['has_changes'] = self._detect_changes(processo)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao processar resposta: {str(e)}")
            return {
                'success': False,
                'error': f'Erro ao processar resposta: {str(e)}',
                'process_number': process_number,
                'process_year': process_year
            }
    
    def _detect_changes(self, processo: Dict) -> bool:
        """
        Detecta se houve mudanças significativas no processo
        """
        # Indicadores de mudança
        change_indicators = [
            'nuovo_documento',
            'cambio_stato',
            'nuova_udienza',
            'decreto_emesso',
            'sentenza_pubblicata'
        ]
        
        status = processo.get('stato', '').lower()
        
        # Verificar se há indicadores de mudança
        for indicator in change_indicators:
            if indicator in status:
                return True
        
        # Verificar se há documentos recentes (últimas 24h)
        documents = processo.get('documenti', [])
        if documents:
            # Lógica para verificar documentos recentes
            # (implementação específica dependeria do formato da API)
            pass
        
        return False
    
    def test_credentials(self, uuid: str, token: str) -> Dict:
        """
        Testa se as credenciais são válidas
        """
        try:
            # Fazer uma consulta simples para testar
            test_result = self.query_process("12345", "2024", uuid, token)
            
            if test_result.get('status_code') == 401:
                return {
                    'success': False,
                    'message': 'Credenciais inválidas ou expiradas'
                }
            elif test_result.get('status_code') == 429:
                return {
                    'success': False,
                    'message': 'Rate limit excedido. Tente novamente mais tarde.'
                }
            elif test_result.get('success') or test_result.get('error') == 'Processo não encontrado':
                # Se conseguiu fazer a consulta (mesmo que não encontrou o processo), as credenciais são válidas
                return {
                    'success': True,
                    'message': 'Credenciais válidas e funcionando'
                }
            else:
                return {
                    'success': False,
                    'message': f'Erro no teste: {test_result.get("error", "Erro desconhecido")}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao testar credenciais: {str(e)}'
            }
    
    def batch_query(self, queries: List[Dict], credentials: List[Dict]) -> List[Dict]:
        """
        Executa múltiplas consultas usando pool de credenciais
        
        Args:
            queries: Lista de dicionários com process_number, process_year, client_id
            credentials: Lista de credenciais disponíveis
            
        Returns:
            Lista com resultados das consultas
        """
        results = []
        credential_index = 0
        
        for query in queries:
            if not credentials:
                results.append({
                    'success': False,
                    'error': 'Nenhuma credencial disponível',
                    'client_id': query.get('client_id'),
                    'process_number': query.get('process_number'),
                    'process_year': query.get('process_year')
                })
                continue
            
            # Usar credencial em rotação
            credential = credentials[credential_index % len(credentials)]
            
            result = self.query_process(
                query['process_number'],
                query['process_year'],
                credential['uuid'],
                credential['token']
            )
            
            # Adicionar informações do cliente
            result['client_id'] = query.get('client_id')
            result['client_name'] = query.get('client_name')
            
            results.append(result)
            
            # Próxima credencial
            credential_index += 1
            
            # Rate limiting entre consultas
            time.sleep(self.rate_limit_delay)
        
        return results
    
    def get_rate_limit_info(self) -> Dict:
        """
        Retorna informações sobre rate limiting
        """
        return {
            'requests_per_minute': 60,
            'delay_between_requests': self.rate_limit_delay,
            'max_retries': self.max_retries,
            'timeout': self.timeout,
            'recommendation': 'Use múltiplas credenciais para aumentar a capacidade'
        }

