import React, { useState } from 'react';
import config from '../config';

const Credentials = ({ credentials, setCredentials, loadCredentials }) => {
  const [showModal, setShowModal] = useState(false);
  const [editingCredential, setEditingCredential] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    uuid: '',
    token: '',
    device_type: 'iPhone'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.uuid || !formData.token) {
      alert('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    try {
      const url = editingCredential 
        ? `${config.API_BASE_URL}/api/credentials/${editingCredential.id}`
        : `${config.API_BASE_URL}/api/credentials`;
      
      const method = editingCredential ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await loadCredentials();
        setShowModal(false);
        setEditingCredential(null);
        setFormData({
          name: '',
          uuid: '',
          token: '',
          device_type: 'iPhone'
        });
        alert(editingCredential ? 'Credencial atualizada com sucesso!' : 'Credencial adicionada com sucesso!');
      } else {
        alert('Erro ao salvar credencial');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
    }
  };

  const handleEdit = (credential) => {
    setEditingCredential(credential);
    setFormData({
      name: credential.name || '',
      uuid: credential.uuid || '',
      token: credential.token || '',
      device_type: credential.device_type || 'iPhone'
    });
    setShowModal(true);
  };

  const handleDelete = async (credential) => {
    if (window.confirm(`Tem certeza que deseja excluir a credencial "${credential.name}"? Esta ação não pode ser desfeita.`)) {
      try {
        const response = await fetch(`${config.API_BASE_URL}/api/credentials/${credential.id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await loadCredentials();
          alert('Credencial excluída com sucesso!');
        } else {
          alert('Erro ao excluir credencial');
        }
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
      }
    }
  };

  const testCredential = async (credential) => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/credentials/${credential.id}/test`, {
        method: 'POST',
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Teste da credencial: ${result.success ? 'SUCESSO' : 'FALHA'}\n${result.message}`);
      } else {
        alert('Erro ao testar credencial');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return '#10b981';
      case 'inactive': return '#ef4444';
      case 'testing': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return 'Ativo';
      case 'inactive': return 'Inativo';
      case 'testing': return 'Testando';
      default: return 'Desconhecido';
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
            Credenciais
          </h1>
          <p style={{ color: '#6b7280', margin: 0 }}>
            Gerencie suas credenciais da API Giustizia Civile
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontSize: '0.875rem',
            fontWeight: '500',
            cursor: 'pointer',
          }}
        >
          + Adicionar Credencial
        </button>
      </div>

      {/* Informações sobre Credenciais */}
      <div style={{
        backgroundColor: '#eff6ff',
        border: '1px solid #dbeafe',
        borderRadius: '0.5rem',
        padding: '1rem',
        marginBottom: '2rem',
      }}>
        <h3 style={{ margin: '0 0 0.5rem 0', color: '#1e40af', fontSize: '1rem', fontWeight: '600' }}>
          💡 Como obter suas credenciais
        </h3>
        <p style={{ margin: 0, color: '#1e40af', fontSize: '0.875rem', lineHeight: '1.5' }}>
          Para obter o UUID e Token, você precisa interceptar o tráfego do app oficial da Giustizia Civile. 
          Consulte o guia de credenciais para instruções detalhadas sobre como extrair essas informações.
        </p>
      </div>

      {/* Lista de Credenciais */}
      <div style={{
        backgroundColor: '#ffffff',
        borderRadius: '0.5rem',
        border: '1px solid #e5e7eb',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
        overflow: 'hidden',
      }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f9fafb' }}>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Nome
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Dispositivo
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  UUID
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Status
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Último Uso
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'center', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Ações
                </th>
              </tr>
            </thead>
            <tbody>
              {credentials.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ 
                    padding: '2rem', 
                    textAlign: 'center', 
                    color: '#6b7280',
                    fontSize: '0.875rem'
                  }}>
                    Nenhuma credencial cadastrada. Adicione sua primeira credencial para começar.
                  </td>
                </tr>
              ) : (
                credentials.map((credential, index) => (
                  <tr key={credential.id} style={{ 
                    borderBottom: index < credentials.length - 1 ? '1px solid #e5e7eb' : 'none' 
                  }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937', fontWeight: '500' }}>
                      {credential.name}
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        backgroundColor: '#f3f4f6',
                        borderRadius: '0.375rem',
                        fontSize: '0.75rem',
                      }}>
                        {credential.device_type}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.75rem', color: '#6b7280', fontFamily: 'monospace' }}>
                      {credential.uuid ? `${credential.uuid.substring(0, 8)}...` : '-'}
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.375rem',
                        fontSize: '0.75rem',
                        fontWeight: '500',
                        backgroundColor: `${getStatusColor(credential.status || 'active')}20`,
                        color: getStatusColor(credential.status || 'active'),
                      }}>
                        {getStatusText(credential.status || 'active')}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#6b7280' }}>
                      {credential.last_used ? new Date(credential.last_used).toLocaleString('pt-BR') : 'Nunca'}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                        <button
                          onClick={() => testCredential(credential)}
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
                          Testar
                        </button>
                        <button
                          onClick={() => handleEdit(credential)}
                          style={{
                            padding: '0.375rem 0.75rem',
                            fontSize: '0.75rem',
                            backgroundColor: '#f59e0b',
                            color: 'white',
                            border: 'none',
                            borderRadius: '0.375rem',
                            cursor: 'pointer',
                          }}
                        >
                          Editar
                        </button>
                        <button
                          onClick={() => handleDelete(credential)}
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
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal Adicionar/Editar Credencial */}
      {showModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
        }}>
          <div style={{
            backgroundColor: 'white',
            padding: '2rem',
            borderRadius: '0.5rem',
            width: '90%',
            maxWidth: '500px',
            maxHeight: '90vh',
            overflowY: 'auto',
          }}>
            <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
              {editingCredential ? 'Editar Credencial' : 'Adicionar Credencial'}
            </h2>
            
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Nome da Credencial *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  placeholder="Ex: Meu iPhone, Tablet Principal"
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  UUID *
                </label>
                <input
                  type="text"
                  value={formData.uuid}
                  onChange={(e) => setFormData({...formData, uuid: e.target.value})}
                  placeholder="550e8400-e29b-41d4-a716-446655440000"
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                    fontFamily: 'monospace',
                    fontSize: '0.875rem',
                  }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Token *
                </label>
                <textarea
                  value={formData.token}
                  onChange={(e) => setFormData({...formData, token: e.target.value})}
                  placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                  rows="4"
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                    fontFamily: 'monospace',
                    fontSize: '0.875rem',
                    resize: 'vertical',
                  }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Tipo de Dispositivo
                </label>
                <select
                  value={formData.device_type}
                  onChange={(e) => setFormData({...formData, device_type: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                >
                  <option value="iPhone">iPhone</option>
                  <option value="iPad">iPad</option>
                  <option value="Android">Android</option>
                  <option value="Tablet Android">Tablet Android</option>
                </select>
              </div>

              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingCredential(null);
                    setFormData({
                      name: '',
                      uuid: '',
                      token: '',
                      device_type: 'iPhone'
                    });
                  }}
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#6b7280',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  style={{
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '0.375rem',
                    cursor: 'pointer',
                  }}
                >
                  {editingCredential ? 'Atualizar' : 'Adicionar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Credentials;

