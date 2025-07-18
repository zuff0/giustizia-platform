import React, { useState, useEffect } from 'react';
import config from '../config';

const Header = () => {
  const [systemStatus, setSystemStatus] = useState('checking');
  const [lastUpdate, setLastUpdate] = useState(null);

  // Verificar status do sistema
  const checkSystemStatus = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 5000,
      });
      
      if (response.ok) {
        setSystemStatus('online');
        setLastUpdate(new Date().toLocaleString('pt-BR'));
      } else {
        setSystemStatus('offline');
      }
    } catch (error) {
      console.error('Erro ao verificar status:', error);
      setSystemStatus('offline');
    }
  };

  useEffect(() => {
    checkSystemStatus();
    const interval = setInterval(checkSystemStatus, 30000); // Verifica a cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (systemStatus) {
      case 'online': return '#10b981';
      case 'offline': return '#ef4444';
      default: return '#f59e0b';
    }
  };

  const getStatusText = () => {
    switch (systemStatus) {
      case 'online': return 'Sistema Online';
      case 'offline': return 'Sistema Offline';
      default: return 'Verificando...';
    }
  };

  return (
    <header style={{
      backgroundColor: '#1f2937',
      color: 'white',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h1 style={{ 
          margin: 0, 
          fontSize: '1.5rem', 
          fontWeight: 'bold',
          color: '#3b82f6'
        }}>
          ⚖️ Giustizia Civile
        </h1>
        <span style={{ 
          fontSize: '0.875rem', 
          color: '#9ca3af',
          backgroundColor: '#374151',
          padding: '0.25rem 0.5rem',
          borderRadius: '0.375rem'
        }}>
          Automação de Consultas
        </span>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: getStatusColor(),
            animation: systemStatus === 'online' ? 'pulse 2s infinite' : 'none',
          }}></div>
          <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>
            {getStatusText()}
          </span>
        </div>
        
        {lastUpdate && (
          <div style={{ 
            fontSize: '0.75rem', 
            color: '#9ca3af',
            textAlign: 'right'
          }}>
            <div>Última verificação:</div>
            <div>{lastUpdate}</div>
          </div>
        )}
      </div>

      <style jsx>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </header>
  );
};

export default Header;

