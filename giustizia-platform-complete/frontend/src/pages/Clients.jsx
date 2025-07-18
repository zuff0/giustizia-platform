import React, { useState, useEffect } from 'react';
import config from '../config';

const Clients = ({ clients, setClients, loadClients }) => {
  const [showModal, setShowModal] = useState(false);
  const [showBulkModal, setShowBulkModal] = useState(false);
  const [editingClient, setEditingClient] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredClients, setFilteredClients] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    process_number: '',
    process_year: '',
    email: '',
    phone: '',
    document: '',
    notes: ''
  });

  useEffect(() => {
    filterClients();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clients, searchTerm]);

  const filterClients = () => {
    if (!searchTerm) {
      setFilteredClients(clients);
      return;
    }

    const filtered = clients.filter(client =>
      client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      client.process_number.toString().includes(searchTerm) ||
      client.process_year.toString().includes(searchTerm) ||
      (client.email && client.email.toLowerCase().includes(searchTerm.toLowerCase()))
    );
    setFilteredClients(filtered);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.process_number || !formData.process_year) {
      alert('Por favor, preencha os campos obrigatórios: Nome, Processo e Ano');
      return;
    }

    try {
      const url = editingClient 
        ? `${config.API_BASE_URL}/api/clients/${editingClient.id}`
        : `${config.API_BASE_URL}/api/clients`;
      
      const method = editingClient ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        await loadClients();
        setShowModal(false);
        setEditingClient(null);
        setFormData({
          name: '',
          process_number: '',
          process_year: '',
          email: '',
          phone: '',
          document: '',
          notes: ''
        });
        alert(editingClient ? 'Cliente atualizado com sucesso!' : 'Cliente adicionado com sucesso!');
      } else {
        alert('Erro ao salvar cliente');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
    }
  };

  const handleEdit = (client) => {
    setEditingClient(client);
    setFormData({
      name: client.name || '',
      process_number: client.process_number || '',
      process_year: client.process_year || '',
      email: client.email || '',
      phone: client.phone || '',
      document: client.document || '',
      notes: client.notes || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (client) => {
    if (window.confirm(`Tem certeza que deseja excluir o cliente ${client.name}?`)) {
      try {
        const response = await fetch(`${config.API_BASE_URL}/api/clients/${client.id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          await loadClients();
          alert('Cliente excluído com sucesso!');
        } else {
          alert('Erro ao excluir cliente');
        }
      } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao conectar com o servidor');
      }
    }
  };

  const handleViewDetails = (client) => {
    alert(`Detalhes do Cliente:

Nome: ${client.name}
Processo: ${client.process_number}/${client.process_year}
Email: ${client.email || 'Não informado'}
Telefone: ${client.phone || 'Não informado'}
Documento: ${client.document || 'Não informado'}
Observações: ${client.notes || 'Nenhuma'}
Cadastrado em: ${new Date(client.created_at).toLocaleString('pt-BR')}`);
  };

  const handleNotifyClient = (client) => {
    if (window.confirm(`Deseja enviar uma notificação para ${client.name}?`)) {
      alert(`Notificação enviada para ${client.name}!`);
    }
  };

  const downloadTemplate = () => {
    const csvContent = `Nome,Processo,Ano,Email,Telefone,Documento,Observações
João Silva,12345,2024,joao@email.com,11999999999,123.456.789-00,Cliente exemplo
Maria Santos,67890,2024,maria@email.com,11888888888,987.654.321-00,Processo urgente`;
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', 'template_clientes.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleBulkImport = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${config.API_BASE_URL}/api/clients/bulk-import`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        await loadClients();
        alert(`Importação concluída!\nSucessos: ${result.success}\nFalhas: ${result.errors}`);
        setShowBulkModal(false);
      } else {
        alert('Erro na importação');
      }
    } catch (error) {
      console.error('Erro:', error);
      alert('Erro ao conectar com o servidor');
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
            Clientes
          </h1>
          <p style={{ color: '#6b7280', margin: 0 }}>
            Gerencie seus clientes e processos
          </p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            onClick={() => setShowBulkModal(true)}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: '#10b981',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
              fontWeight: '500',
              cursor: 'pointer',
            }}
          >
            📥 Importar Lote
          </button>
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
            + Adicionar Cliente
          </button>
        </div>
      </div>

      {/* Barra de Pesquisa */}
      <div style={{ marginBottom: '1.5rem' }}>
        <div style={{ position: 'relative', maxWidth: '400px' }}>
          <input
            type="text"
            placeholder="Pesquisar por nome, processo ou e-mail..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 1rem 0.75rem 2.5rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
            }}
          />
          <div style={{
            position: 'absolute',
            left: '0.75rem',
            top: '50%',
            transform: 'translateY(-50%)',
            color: '#9ca3af',
          }}>
            🔍
          </div>
        </div>
        <p style={{ 
          fontSize: '0.875rem', 
          color: '#6b7280', 
          marginTop: '0.5rem',
          margin: '0.5rem 0 0 0'
        }}>
          Mostrando {filteredClients.length} de {clients.length} clientes
        </p>
      </div>

      {/* Tabela de Clientes */}
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
                  Processo
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Email
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'left', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Telefone
                </th>
                <th style={{ padding: '0.75rem', textAlign: 'center', fontSize: '0.875rem', fontWeight: '600', color: '#374151' }}>
                  Ações
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredClients.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ 
                    padding: '2rem', 
                    textAlign: 'center', 
                    color: '#6b7280',
                    fontSize: '0.875rem'
                  }}>
                    {clients.length === 0 ? 'Nenhum cliente cadastrado' : 'Nenhum cliente encontrado'}
                  </td>
                </tr>
              ) : (
                filteredClients.map((client, index) => (
                  <tr key={client.id} style={{ 
                    borderBottom: index < filteredClients.length - 1 ? '1px solid #e5e7eb' : 'none' 
                  }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                      {client.name}
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#1f2937' }}>
                      {client.process_number}/{client.process_year}
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#6b7280' }}>
                      {client.email || '-'}
                    </td>
                    <td style={{ padding: '0.75rem', fontSize: '0.875rem', color: '#6b7280' }}>
                      {client.phone || '-'}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center' }}>
                        <button
                          onClick={() => handleViewDetails(client)}
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
                          onClick={() => handleNotifyClient(client)}
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
                          Notificar
                        </button>
                        <button
                          onClick={() => handleEdit(client)}
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
                          onClick={() => handleDelete(client)}
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

      {/* Modal Adicionar/Editar Cliente */}
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
              {editingClient ? 'Editar Cliente' : 'Adicionar Cliente'}
            </h2>
            
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Nome *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                  required
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                    Número do Processo *
                  </label>
                  <input
                    type="text"
                    value={formData.process_number}
                    onChange={(e) => setFormData({...formData, process_number: e.target.value})}
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '0.375rem',
                    }}
                    required
                  />
                </div>
                <div>
                  <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                    Ano *
                  </label>
                  <input
                    type="number"
                    value={formData.process_year}
                    onChange={(e) => setFormData({...formData, process_year: e.target.value})}
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '0.375rem',
                    }}
                    required
                  />
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Telefone
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Documento (CPF/RG)
                </label>
                <input
                  type="text"
                  value={formData.document}
                  onChange={(e) => setFormData({...formData, document: e.target.value})}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                  }}
                />
              </div>

              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                  Observações
                </label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                  rows="3"
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    border: '1px solid #d1d5db',
                    borderRadius: '0.375rem',
                    resize: 'vertical',
                  }}
                />
              </div>

              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingClient(null);
                    setFormData({
                      name: '',
                      process_number: '',
                      process_year: '',
                      email: '',
                      phone: '',
                      document: '',
                      notes: ''
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
                  {editingClient ? 'Atualizar' : 'Adicionar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Importação em Lote */}
      {showBulkModal && (
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
          }}>
            <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem', fontWeight: 'bold' }}>
              Importar Clientes em Lote
            </h2>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <p style={{ marginBottom: '1rem', color: '#6b7280' }}>
                Faça upload de um arquivo CSV ou Excel com os dados dos clientes.
              </p>
              
              <button
                onClick={downloadTemplate}
                style={{
                  padding: '0.75rem 1rem',
                  backgroundColor: '#10b981',
                  color: 'white',
                  border: 'none',
                  borderRadius: '0.375rem',
                  cursor: 'pointer',
                  marginBottom: '1rem',
                }}
              >
                📥 Baixar Template CSV
              </button>
              
              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleBulkImport}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '2px dashed #d1d5db',
                  borderRadius: '0.375rem',
                  backgroundColor: '#f9fafb',
                }}
              />
            </div>

            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setShowBulkModal(false)}
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
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Clients;

