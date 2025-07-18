import React, { useState, useEffect } from 'react';
import config from '../config';

const Settings = () => {
  const [settings, setSettings] = useState({
    email_notifications: true,
    daily_queries: true,
    notification_email: 'admin@empresa.com',
    query_time: '08:00',
    max_retries: 3,
    timeout_seconds: 30,
    batch_size: 10,
  });
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/settings`);
      if (response.ok) {
        const data = await response.json();
        setSettings(prev => ({ ...prev, ...data }));
      }
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSaved(false);

    try {
      const response = await fetch(`${config.API_BASE_URL}/api/settings`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });

      if (response.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      } else {
        alert('Erro ao salvar configurações');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
    } finally {
      setLoading(false);
    }
  };

  const testEmailNotification = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/test-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: settings.notification_email }),
      });

      if (response.ok) {
        alert('E-mail de teste enviado com sucesso!');
      } else {
        alert('Erro ao enviar e-mail de teste');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
    }
  };

  const runManualQuery = async () => {
    if (window.confirm('Deseja executar uma consulta manual agora? Isso pode levar alguns minutos.')) {
      try {
        const response = await fetch(`${config.API_BASE_URL}/api/manual-query`, {
          method: 'POST',
        });

        if (response.ok) {
          alert('Consulta manual iniciada! Verifique as notificações para acompanhar o progresso.');
        } else {
          alert('Erro ao iniciar consulta manual');
        }
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
      }
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
          Configurações
        </h1>
        <p style={{ color: '#6b7280', margin: 0 }}>
          Configure o comportamento do sistema de automação
        </p>
      </div>

      <form onSubmit={handleSave}>
        {/* Configurações de Notificação */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          padding: '1.5rem',
          marginBottom: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            fontWeight: '600', 
            color: '#1f2937',
            marginBottom: '1rem'
          }}>
            📧 Notificações por E-mail
          </h2>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              marginBottom: '1rem',
            }}>
              <input
                type="checkbox"
                checked={settings.email_notifications}
                onChange={(e) => setSettings({...settings, email_notifications: e.target.checked})}
                style={{ width: '16px', height: '16px' }}
              />
              <span style={{ fontSize: '0.875rem', color: '#374151' }}>
                Enviar notificações por e-mail
              </span>
            </label>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                E-mail para Notificações
              </label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input
                  type="email"
                  value={settings.notification_email}
                  onChange={(e) => setSettings({...settings, notification_email: e.target.value})}
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                  required
                />
                <button
                  type="button"
                  onClick={testEmailNotification}
                  style={{
                    padding: '0.75rem 1rem',
                    backgroundColor: '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    fontSize: '0.875rem',
                    cursor: 'pointer',
                  }}
                >
                  Testar
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Configurações de Consulta */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          padding: '1.5rem',
          marginBottom: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            fontWeight: '600', 
            color: '#1f2937',
            marginBottom: '1rem'
          }}>
            🕐 Agendamento de Consultas
          </h2>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              marginBottom: '1rem',
            }}>
              <input
                type="checkbox"
                checked={settings.daily_queries}
                onChange={(e) => setSettings({...settings, daily_queries: e.target.checked})}
                style={{ width: '16px', height: '16px' }}
              />
              <span style={{ fontSize: '0.875rem', color: '#374151' }}>
                Executar consultas automáticas diariamente
              </span>
            </label>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Horário das Consultas
                </label>
                <input
                  type="time"
                  value={settings.query_time}
                  onChange={(e) => setSettings({...settings, query_time: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Tamanho do Lote
                </label>
                <input
                  type="number"
                  min="1"
                  max="50"
                  value={settings.batch_size}
                  onChange={(e) => setSettings({...settings, batch_size: parseInt(e.target.value)})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                />
              </div>
            </div>

            <div style={{ marginTop: '1rem' }}>
              <button
                type="button"
                onClick={runManualQuery}
                style={{
                  padding: '0.75rem 1.5rem',
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                }}
              >
                🚀 Executar Consulta Manual
              </button>
            </div>
          </div>
        </div>

        {/* Configurações Técnicas */}
        <div style={{
          backgroundColor: '#ffffff',
          borderRadius: '0.5rem',
          border: '1px solid #e5e7eb',
          padding: '1.5rem',
          marginBottom: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        }}>
          <h2 style={{ 
            fontSize: '1.25rem', 
            fontWeight: '600', 
            color: '#1f2937',
            marginBottom: '1rem'
          }}>
            ⚙️ Configurações Técnicas
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                Máximo de Tentativas
              </label>
              <input
                type="number"
                min="1"
                max="10"
                value={settings.max_retries}
                onChange={(e) => setSettings({...settings, max_retries: parseInt(e.target.value)})}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                }}
              />
              <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0 0 0' }}>
                Número de tentativas em caso de falha
              </p>
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                Timeout (segundos)
              </label>
              <input
                type="number"
                min="10"
                max="120"
                value={settings.timeout_seconds}
                onChange={(e) => setSettings({...settings, timeout_seconds: parseInt(e.target.value)})}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '0.375rem',
                }}
              />
              <p style={{ fontSize: '0.75rem', color: '#6b7280', margin: '0.25rem 0 0 0' }}>
                Tempo limite para cada consulta
              </p>
            </div>
          </div>
        </div>

        {/* Botão Salvar */}
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '0.75rem 2rem',
              backgroundColor: loading ? '#9ca3af' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontSize: '1rem',
              fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Salvando...' : 'Salvar Configurações'}
          </button>

          {saved && (
            <span style={{
              color: '#10b981',
              fontSize: '0.875rem',
              fontWeight: '500',
            }}>
              ✅ Configurações salvas com sucesso!
            </span>
          )}
        </div>
      </form>

      {/* Informações do Sistema */}
      <div style={{
        backgroundColor: '#f9fafb',
        borderRadius: '0.5rem',
        border: '1px solid #e5e7eb',
        padding: '1.5rem',
        marginTop: '2rem',
      }}>
        <h3 style={{ 
          fontSize: '1.125rem', 
          fontWeight: '600', 
          color: '#1f2937',
          marginBottom: '1rem'
        }}>
          ℹ️ Informações do Sistema
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>Versão</div>
            <div style={{ fontSize: '1rem', fontWeight: '500', color: '#1f2937' }}>
              {config.VERSION}
            </div>
          </div>
          
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>API Base URL</div>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: '#1f2937', fontFamily: 'monospace' }}>
              {config.API_BASE_URL}
            </div>
          </div>
          
          <div>
            <div style={{ fontSize: '0.875rem', color: '#6b7280' }}>Timeout da API</div>
            <div style={{ fontSize: '1rem', fontWeight: '500', color: '#1f2937' }}>
              {config.API_TIMEOUT / 1000}s
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;

