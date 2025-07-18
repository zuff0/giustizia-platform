import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Clients from './pages/Clients';
import Credentials from './pages/Credentials';
import Notifications from './pages/Notifications';
import Settings from './pages/Settings';
import config from './config';

function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [clients, setClients] = useState([]);
  const [credentials, setCredentials] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  // Carregar dados iniciais
  useEffect(() => {
    loadInitialData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        loadClients(),
        loadCredentials(),
        loadNotifications()
      ]);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadClients = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/clients`);
      if (response.ok) {
        const data = await response.json();
        setClients(data);
      }
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
      setClients([]);
    }
  };

  const loadCredentials = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/credentials`);
      if (response.ok) {
        const data = await response.json();
        setCredentials(data);
      }
    } catch (error) {
      console.error('Erro ao carregar credenciais:', error);
      setCredentials([]);
    }
  };

  const loadNotifications = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/notifications`);
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      console.error('Erro ao carregar notificações:', error);
      setNotifications([]);
    }
  };

  const renderActiveSection = () => {
    const commonProps = {
      clients,
      credentials,
      notifications,
      setClients,
      setCredentials,
      setNotifications,
      loadClients,
      loadCredentials,
      loadNotifications,
    };

    switch (activeSection) {
      case 'dashboard':
        return <Dashboard {...commonProps} />;
      case 'clients':
        return <Clients {...commonProps} />;
      case 'credentials':
        return <Credentials {...commonProps} />;
      case 'notifications':
        return <Notifications {...commonProps} />;
      case 'settings':
        return <Settings {...commonProps} />;
      default:
        return <Dashboard {...commonProps} />;
    }
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f9fafb',
      }}>
        <div style={{
          textAlign: 'center',
          padding: '2rem',
        }}>
          <div style={{
            width: '40px',
            height: '40px',
            border: '4px solid #e5e7eb',
            borderTop: '4px solid #3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem',
          }}></div>
          <p style={{ color: '#6b7280', fontSize: '1rem' }}>
            Carregando plataforma...
          </p>
        </div>
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div style={{ 
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      backgroundColor: '#ffffff',
      minHeight: '100vh',
    }}>
      <Header />
      <div style={{ display: 'flex' }}>
        <Sidebar 
          activeSection={activeSection} 
          setActiveSection={setActiveSection} 
        />
        <main style={{
          flex: 1,
          padding: '2rem',
          backgroundColor: '#ffffff',
          minHeight: 'calc(100vh - 80px)',
        }}>
          {renderActiveSection()}
        </main>
      </div>
    </div>
  );
}

export default App;

