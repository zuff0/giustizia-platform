import React, { useState, useEffect } from 'react';
import config from '../config';

const Notifications = ({ notifications, loadNotifications }) => {
  const [filter, setFilter] = useState('all');
  const [filteredNotifications, setFilteredNotifications] = useState([]);

  useEffect(() => {
    filterNotifications();
  }, [notifications, filter]);

  const filterNotifications = () => {
    let filtered = notifications;
    
    if (filter !== 'all') {
      filtered = notifications.filter(notification => notification.type === filter);
    }
    
    // Ordenar por data (mais recente primeiro)
    filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    setFilteredNotifications(filtered);
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'status_change': return '📊';
      case 'error': return '❌';
      case 'success': return '✅';
      case 'warning': return '⚠️';
      case 'info': return 'ℹ️';
      default: return '🔔';
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'status_change': return '#3b82f6';
      case 'error': return '#ef4444';
      case 'success': return '#10b981';
      case 'warning': return '#f59e0b';
      case 'info': return '#6b7280';
      default: return '#6b7280';
    }
  };

  const getTypeLabel = (type) => {
    switch (type) {
      case 'status_change': return 'Mudança de Status';
      case 'error': return 'Erro';
      case 'success': return 'Sucesso';
      case 'warning': return 'Aviso';
      case 'info': return 'Informação';
      default: return 'Notificação';
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/notifications/${notificationId}/read`, {
        method: 'PUT',
      });

      if (response.ok) {
        await loadNotifications();
      }
    } catch (error) {
      console.error('Erro ao marcar como lida:', error);
    }
  };

  const deleteNotification = async (notificationId) => {
    if (window.confirm('Tem certeza que deseja excluir esta notificação?')) {
      try {
        const response = await fetch(`${config.API_BASE_URL}/api/notifications/${notificationId}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await loadNotifications();
        }
      } catch (error) {
        console.error('Erro ao excluir notificação:', error);
      }
    }
  };

  const clearAllNotifications = async () => {
    if (window.confirm('Tem certeza que deseja limpar todas as notificações?')) {
      try {
        const response = await fetch(`${config.API_BASE_URL}/api/notifications/clear`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await loadNotifications();
        }
      } catch (error) {
        console.error('Erro ao limpar notificações:', error);
      }
    }
  };

  return (
    <div>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem' 
      }}>
        <div>
          <h1 style={{ 
            fontSize: '2rem', 
            fontWeight: 'bold', 
            color: '#1f2937',
            margin: '0 0 0.5rem 0'
          }}>
            Notificações
          </h1>
          <p style={{ color: '#6b7280', margin: 0 }}>
            Acompanhe todas as atividades do sistema
          </p>
        </div>
        {notifications.length > 0 && (
          <button
            onClick={clearAllNotifications}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: '#ef4444',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              cursor: 'pointer',
            }}
          >
            Limpar Todas
          </button>
        )}
      </div>

      {/* Filtros */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {[
            { value: 'all', label: 'Todas' },
            { value: 'status_change', label: 'Mudanças de Status' },
            { value: 'error', label: 'Erros' },
            { value: 'success', label: 'Sucessos' },
            { value: 'warning', label: 'Avisos' },
            { value: 'info', label: 'Informações' },
          ].map((filterOption) => (
            <button
              key={filterOption.value}
              onClick={() => setFilter(filterOption.value)}
              style={{
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem',
                backgroundColor: filter === filterOption.value ? '#3b82f6' : 'white',
                color: filter === filterOption.value ? 'white' : '#374151',
                fontSize: '0.875rem',
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
            >
              {filterOption.label}
            </button>
          ))}
        </div>
      </div>

      {/* Lista de Notificações */}
      <div style={{ space: '1rem' }}>
        {filteredNotifications.length === 0 ? (
          <div style={{
            backgroundColor: '#ffffff',
            borderRadius: '0.5rem',
            border: '1px solid #e5e7eb',
            padding: '3rem',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔔</div>
            <h3 style={{ margin: '0 0 0.5rem 0', color: '#1f2937' }}>
              {filter === 'all' ? 'Nenhuma notificação' : `Nenhuma notificação do tipo "${getTypeLabel(filter)}"`}
            </h3>
            <p style={{ margin: 0, color: '#6b7280' }}>
              As notificações aparecerão aqui quando houver atividades no sistema.
            </p>
          </div>
        ) : (
          filteredNotifications.map((notification) => (
            <div
              key={notification.id}
              style={{
                backgroundColor: '#ffffff',
                borderRadius: '0.5rem',
                border: '1px solid #e5e7eb',
                padding: '1.5rem',
                marginBottom: '1rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                opacity: notification.read ? 0.7 : 1,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                <div style={{
                  fontSize: '1.5rem',
                  padding: '0.5rem',
                  backgroundColor: `${getNotificationColor(notification.type)}20`,
                  borderRadius: '0.5rem',
                  flexShrink: 0,
                }}>
                  {getNotificationIcon(notification.type)}
                </div>
                
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.375rem',
                      fontSize: '0.75rem',
                      fontWeight: '500',
                      backgroundColor: `${getNotificationColor(notification.type)}20`,
                      color: getNotificationColor(notification.type),
                    }}>
                      {getTypeLabel(notification.type)}
                    </span>
                    
                    <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                      {new Date(notification.created_at).toLocaleString('pt-BR')}
                    </span>
                    
                    {!notification.read && (
                      <span style={{
                        width: '8px',
                        height: '8px',
                        backgroundColor: '#3b82f6',
                        borderRadius: '50%',
                      }}></span>
                    )}
                  </div>
                  
                  <h3 style={{ 
                    margin: '0 0 0.5rem 0', 
                    fontSize: '1.125rem', 
                    fontWeight: '600',
                    color: '#1f2937'
                  }}>
                    {notification.title}
                  </h3>
                  
                  <p style={{ 
                    margin: '0 0 1rem 0', 
                    color: '#6b7280',
                    lineHeight: '1.5'
                  }}>
                    {notification.message}
                  </p>
                  
                  {notification.client_name && (
                    <div style={{
                      padding: '0.75rem',
                      backgroundColor: '#f9fafb',
                      borderRadius: '0.375rem',
                      marginBottom: '1rem',
                    }}>
                      <div style={{ fontSize: '0.875rem', color: '#374151' }}>
                        <strong>Cliente:</strong> {notification.client_name}
                      </div>
                      {notification.process_number && (
                        <div style={{ fontSize: '0.875rem', color: '#374151' }}>
                          <strong>Processo:</strong> {notification.process_number}
                        </div>
                      )}
                    </div>
                  )}
                </div>
                
                <div style={{ display: 'flex', gap: '0.5rem', flexShrink: 0 }}>
                  {!notification.read && (
                    <button
                      onClick={() => markAsRead(notification.id)}
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
                      Marcar como Lida
                    </button>
                  )}
                  
                  <button
                    onClick={() => deleteNotification(notification.id)}
                    style={{
                      padding: '0.375rem 0.75rem',
                      fontSize: '0.75rem',
                      backgroundColor: '#ef4444',
                      color: 'white',
                      border: 'none',
                      borderRadius: '0.375rem',
                      cursor: 'pointer',
                    }}
                  >
                    Excluir
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Notifications;

