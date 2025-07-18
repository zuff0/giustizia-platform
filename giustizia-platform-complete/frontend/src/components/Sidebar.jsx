import React from 'react';

const Sidebar = ({ activeSection, setActiveSection }) => {
  const menuItems = [
    { 
      id: 'dashboard', 
      label: 'Dashboard', 
      icon: '📊', 
      color: '#10b981',
      number: '1'
    },
    { 
      id: 'clients', 
      label: 'Clientes', 
      icon: '👥', 
      color: '#3b82f6',
      number: '2'
    },
    { 
      id: 'credentials', 
      label: 'Credenciais', 
      icon: '🔑', 
      color: '#f59e0b',
      number: '3'
    },
    { 
      id: 'notifications', 
      label: 'Notificações', 
      icon: '🔔', 
      color: '#8b5cf6',
      number: '4'
    },
    { 
      id: 'settings', 
      label: 'Configurações', 
      icon: '⚙️', 
      color: '#06b6d4',
      number: '5'
    },
  ];

  const handleMenuClick = (sectionId) => {
    setActiveSection(sectionId);
  };

  return (
    <aside style={{
      width: '280px',
      backgroundColor: '#f9fafb',
      borderRight: '1px solid #e5e7eb',
      height: 'calc(100vh - 80px)',
      padding: '1.5rem 0',
      position: 'sticky',
      top: '80px',
      overflowY: 'auto',
    }}>
      <nav>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {menuItems.map((item) => {
            const isActive = activeSection === item.id;
            
            return (
              <li key={item.id} style={{ margin: '0.5rem 1rem' }}>
                <button
                  onClick={() => handleMenuClick(item.id)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.875rem 1rem',
                    border: 'none',
                    borderRadius: '0.5rem',
                    backgroundColor: isActive ? item.color : 'transparent',
                    color: isActive ? 'white' : '#374151',
                    fontSize: '0.875rem',
                    fontWeight: isActive ? '600' : '500',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease-in-out',
                    textAlign: 'left',
                  }}
                  onMouseEnter={(e) => {
                    if (!isActive) {
                      e.target.style.backgroundColor = '#f3f4f6';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) {
                      e.target.style.backgroundColor = 'transparent';
                    }
                  }}
                >
                  <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    backgroundColor: isActive ? 'rgba(255,255,255,0.2)' : item.color,
                    color: isActive ? 'white' : 'white',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                  }}>
                    {item.number}
                  </span>
                  
                  <span style={{ fontSize: '1.25rem' }}>
                    {item.icon}
                  </span>
                  
                  <span style={{ flex: 1 }}>
                    {item.label}
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div style={{
        margin: '2rem 1rem 1rem',
        padding: '1rem',
        backgroundColor: '#eff6ff',
        borderRadius: '0.5rem',
        border: '1px solid #dbeafe',
      }}>
        <div style={{
          fontSize: '0.75rem',
          color: '#1e40af',
          fontWeight: '600',
          marginBottom: '0.5rem',
        }}>
          💡 Dica
        </div>
        <div style={{
          fontSize: '0.75rem',
          color: '#1e40af',
          lineHeight: '1.4',
        }}>
          Configure suas credenciais e adicione clientes para começar a monitorar processos automaticamente.
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;

