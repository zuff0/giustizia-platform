// Configuração da API
const config = {
  // URL do backend - ALTERE AQUI após fazer deploy do backend
  API_BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // Configurações da aplicação
  APP_NAME: 'Giustizia Civile',
  VERSION: '1.0.0',
  
  // Configurações de timeout
  API_TIMEOUT: 30000, // 30 segundos
  
  // Configurações de paginação
  ITEMS_PER_PAGE: 10,
  
  // Configurações de notificação
  NOTIFICATION_DURATION: 5000, // 5 segundos
};

export default config;

