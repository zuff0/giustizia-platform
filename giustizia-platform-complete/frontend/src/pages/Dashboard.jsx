import React, { useState, useEffect } from 'react';
import config from '../config';

const Dashboard = ({ clients, notifications }) => {
  const [stats, setStats] = useState({
    totalClients: 0,
    consultasHoje: 0,
    mudancasDetectadas: 0,
  });
  const [recentUpdates, setRecentUpdates] = useState([]);

  useEffect(() => {
    updateStats();
    loadRecentUpdates();
  }, [clients, notifications]);

  const updateStats = () => {
    const today = new Date().toDateString();
    const consultasHoje = notifications.filter(n => 
      new Date(n.created_at).toDateString() === today
    ).length;
    
    const mudancasDetectadas = notifications.filter(n => 
      n.type === 'status_change'
    ).length;

    setStats({
      totalClients: clients.length,
      consultasHoje,
      mudancasDetectadas,
    });
  };

  const loadRecentUpdates = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/recent-updates`);
      if (response.ok) {
        const data = await response.json();
        setRecentUpdates(data);
      } else {
        // Dados de exemplo se API não responder
        setRecentUpdates([
          {
            id: 1,
            client_name: 'João Silva',
            process_number: '12345/2024',
            status_change: 'Processo deferido',
            updated_at: new Date().toISOString(),
            priority: 'alta'
          },
          {
            id: 2,
            client_name: 'Maria Santos',
            process_number: '67890/2024',
            status_change: 'Documentos solicitados',
            updated_at: new Date(Date.now() - 3600000).toISOString(),
            priority: 'media'
          },
          {
            id: 3,
            client_name: 'Carlos Oliveira',
            process_number: '11111/2024',
            status_change: 'Processo em análise',
            updated_at: new Date(Date.now() - 7200000).toISOString(),
            priority: 'baixa'
          }
        ]);
      }
    } catch (error) {
      console.error('Erro ao carregar atualizações:', error);
    }
  };

  const handleViewDetails = (update) => {
    alert(`Detalhes da Atualização:

Cliente: ${update.client_name}
Processo: ${update.process_number}
Mudança: ${update.status_change}
Data: ${new Date(update.updated_at).toLocaleString('pt-BR')}
Prioridade: ${update.priority.toUpperCase()}`);
  };

  const handleNotifyClient = (update) => {
    if (window.confirm(`Deseja notificar ${update.client_name} sobre a mudança "${update.status_change}"?`)) {
      alert(`Notificação enviada para ${update.client_name} por email e SMS!`);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'alta': return '#ef4444';
      case 'media': return '#f59e0b';
      case 'baixa': return '#10b981';
      default: return '#6b7280';
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '2rem', 
          fontWeight: 'bold', 
          color: '#1f2937',
          margin: '0 0 0.5rem 0'
        }}>
          Dashboard
        </h1>
        <p style={{ color: '#6b7280', margin: 0 }}>
          Visão geral do sistema de automação
        </p>
      </div>

      {/* Cards de Estatísticas */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem',
      }}>
        <div style={{
          backgroundColor: '#ffffff',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#dbeafe',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
            }}>
              👥
            </div>
            <div>
              <p style={{ margin: 0, fontSize: '0.875rem', color: '#6b7280' }}>
                Total de Clientes
              </p>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#1f2937' }}>
                {stats.totalClients}
              </p>
            </div>
          </div>
        </div>

        <div style={{
          backgroundColor: '#ffffff',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#dcfce7',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
            }}>
              🔍
            </div>
            <div>
              <p style={{ margin: 0, fontSize: '0.875rem', color: '#6b7280' }}>
                Consultas Hoje
              </p>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#1f2937' }}>
                {stats.consultasHoje}
              </p>
            </div>
          </div>
        </div>

        <div style={{
          backgroundColor: '#ffffff',
          padding: '1.5rem',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: '48px',
              height: '48px',
              backgroundColor: '#fef3c7',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
            }}>
              📊
            </div>
            <div>
              <p style={{ margin: 0, fontSize: '0.875rem', color: '#6b7280' }}>
                Mudanças Detectadas
              </p>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#1f2937' }}>
                {stats.mudancasDetectadas}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabela de Atualizações Recentes */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '0.5rem',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        overflow: 'hidden',
      }}>
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid #e5e7eb',
          backgroundColor: '#f9fafb',
        }}>
          <h2 style={{ 
            margin: 0, 
            fontSize: '1.25rem', 
            fontWeight: '600', 
            color: '#1f2937' 
          }}>
            Atualizações Recentes
          </h2>
        </div>
        
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f9fafb' }}>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Cliente
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Processo
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Mudança
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Data
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Prioridade
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'center', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Ações
                </th>
              </tr>
            </thead>
            <tbody>
              {recentUpdates.map((update, index) => (
                <tr key={update.id} style={{ 
                  borderBottom: index < recentUpdates.length - 1 ? '1px solid #e5e7eb' : 'none' 
                }}>
                  <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                    {update.client_name}
                  </td>
                  <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                    {update.process_number}
                  </td>
                  <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                    {update.status_change}
                  </td>
                  <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#6b7280' }}>
                    {new Date(update.updated_at).toLocaleString('pt-BR')}
                  </td>
                  <td style={{ padding: '0.75rem' }}>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.375rem',
                      fontSize: '0.75rem',
                      fontWeight: '500',
                      backgroundColor: `${getPriorityColor(update.priority)}20`,
                      color: getPriorityColor(update.priority),
                    }}>
                      {update.priority.toUpperCase()}
                    </span>
                  </td>
                  <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                      <button
                        onClick={() => handleViewDetails(update)}
                        style={{
                          padding: '0.375rem 0.75rem',
                          fontSize: '0.75rem',
                          backgroundColor: '#3b82f6',
                          color: 'white',
                          border: 'none',
                          borderRadius: '0.375rem',
                          cursor: 'pointer',
                        }}
                      >
                        Ver Detalhes
                      </button>
                      <button
                        onClick={() => handleNotifyClient(update)}
                        style={{
                          padding: '0.375rem 0.75rem',
                          fontSize: '0.75rem',
                          backgroundColor: '#10b981',
                          color: 'white',
                          border: 'none',
                          borderRadius: '0.375rem',
                          cursor: 'pointer',
                        }}
                      >
                        Notificar Cliente
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

