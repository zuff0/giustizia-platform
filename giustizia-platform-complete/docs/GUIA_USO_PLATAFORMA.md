# 📖 Guia Completo de Uso - Plataforma Giustizia Civile

**Manual do usuário para operação diária**

Este guia vai te ensinar como usar todas as funcionalidades da sua plataforma de automação após ela estar online.

## 🎯 Visão Geral da Plataforma

### **O que a plataforma faz:**
- 🔍 **Consulta automaticamente** todos os seus processos
- 📧 **Envia notificações** quando há mudanças
- 📊 **Organiza informações** em dashboard intuitivo
- ⏰ **Funciona 24/7** sem intervenção manual
- 📈 **Escala para milhares** de processos

### **Seções principais:**
1. **📊 Dashboard** - Visão geral e estatísticas
2. **👥 Clientes** - Gerenciar clientes e processos
3. **🔑 Credenciais** - Configurar acesso à API
4. **🔔 Notificações** - Acompanhar alertas
5. **⚙️ Configurações** - Personalizar funcionamento

## 📊 SEÇÃO 1: Dashboard

**O Dashboard é sua central de comando - aqui você vê tudo que está acontecendo.**

### **Métricas principais:**

#### **👥 Total de Clientes**
- **O que mostra:** Quantos clientes você tem cadastrados
- **Atualização:** Tempo real (quando você adiciona/remove)
- **Uso:** Acompanhar crescimento da base

#### **🔍 Consultas Hoje**
- **O que mostra:** Quantas consultas foram feitas hoje
- **Atualização:** Incrementa a cada consulta automática
- **Uso:** Verificar se sistema está funcionando

#### **📊 Mudanças Detectadas**
- **O que mostra:** Total de mudanças encontradas
- **Atualização:** Incrementa quando há alterações
- **Uso:** Acompanhar atividade dos processos

### **Tabela de Atualizações Recentes:**

**Colunas:**
- **Cliente:** Nome do cliente
- **Processo:** Número/ano do processo
- **Mudança:** Descrição da alteração
- **Data:** Quando foi detectada
- **Prioridade:** Alta/Média/Baixa

**Ações disponíveis:**
- **👁️ Ver Detalhes:** Mostra informações completas
- **📧 Notificar Cliente:** Envia alerta personalizado

### **Como interpretar:**

**🟢 Sistema funcionando bem:**
- Consultas incrementando diariamente
- Atualizações aparecendo na tabela
- Status "Online" no cabeçalho

**🟡 Atenção necessária:**
- Muitas consultas falhando
- Poucas atualizações (pode ser normal)
- Credenciais expirando

**🔴 Problema crítico:**
- Status "Offline"
- Nenhuma consulta hoje
- Erros nas notificações

## 👥 SEÇÃO 2: Clientes

**Aqui você gerencia todos os seus clientes e processos.**

### **Visualização da lista:**

**Informações mostradas:**
- **Nome:** Nome completo do cliente
- **Processo:** Número/ano (ex: 12345/2024)
- **Email:** Para notificações (opcional)
- **Telefone:** Para contato (opcional)

**Barra de pesquisa:**
- **Busca por:** Nome, processo, email
- **Tempo real:** Filtra conforme você digita
- **Contador:** Mostra "X de Y clientes"

### **Adicionar cliente individual:**

1. **Clique:** "Adicionar Cliente"
2. **Preencha campos obrigatórios:**
   - ✅ **Nome:** Nome completo
   - ✅ **Número do Processo:** Apenas números
   - ✅ **Ano:** Ano do processo
3. **Preencha campos opcionais:**
   - **Email:** Para notificações
   - **Telefone:** Para contato
   - **Documento:** CPF/RG
   - **Observações:** Notas importantes
4. **Clique:** "Adicionar"

### **Importação em lote:**

**Quando usar:**
- Mais de 10 clientes para adicionar
- Dados já organizados em planilha
- Migração de sistema anterior

**Processo:**
1. **Clique:** "Importar Lote"
2. **Baixe template:** Clique "📥 Baixar Template CSV"
3. **Preencha planilha:**
   - **Nome:** Obrigatório
   - **Processo:** Obrigatório (apenas números)
   - **Ano:** Obrigatório
   - **Email, Telefone, Documento, Observações:** Opcionais
4. **Salve como CSV** ou mantenha Excel
5. **Faça upload:** Arraste arquivo ou clique para selecionar
6. **Aguarde processamento**
7. **Veja relatório:** Sucessos e falhas

**Dicas para importação:**
- ✅ **Use template fornecido** (evita erros de formato)
- ✅ **Verifique dados** antes do upload
- ✅ **Processe em lotes** de até 1000 clientes
- ✅ **Mantenha backup** da planilha original

### **Ações com clientes:**

#### **👁️ Ver Detalhes**
- **Mostra:** Todas as informações do cliente
- **Inclui:** Data de cadastro, histórico
- **Uso:** Verificar dados completos

#### **📧 Notificar Cliente**
- **Função:** Enviar alerta personalizado
- **Quando usar:** Mudança importante detectada
- **Processo:** Confirma envio → Envia email/SMS

#### **✏️ Editar**
- **Permite:** Alterar qualquer informação
- **Cuidado:** Mudar processo pode afetar histórico
- **Uso:** Corrigir dados ou atualizar contato

#### **🗑️ Excluir**
- **Ação:** Remove cliente permanentemente
- **Confirmação:** Dupla verificação de segurança
- **Cuidado:** Não pode ser desfeito

## 🔑 SEÇÃO 3: Credenciais

**Aqui você gerencia o acesso à API oficial da Giustizia Civile.**

### **Por que precisa de credenciais:**
- 🔐 **Autenticação:** Prova que você tem acesso legítimo
- ⚡ **Rate limiting:** Cada credencial = 60 consultas/minuto
- 🔄 **Redundância:** Múltiplas credenciais = maior capacidade
- 🛡️ **Segurança:** Tokens expiram periodicamente

### **Informações das credenciais:**

**Campos mostrados:**
- **Nome:** Identificador amigável (ex: "Meu iPhone")
- **Dispositivo:** Tipo (iPhone, Android, iPad)
- **UUID:** Primeiros 8 caracteres (segurança)
- **Status:** Ativo/Inativo/Testando
- **Último Uso:** Quando foi usada pela última vez

### **Adicionar credencial:**

1. **Clique:** "Adicionar Credencial"
2. **Preencha:**
   - **Nome:** Identificador único (ex: "iPhone Principal")
   - **UUID:** Cole o valor extraído (36 caracteres)
   - **Token:** Cole o valor extraído (centenas de caracteres)
   - **Dispositivo:** Selecione o tipo correto
3. **Clique:** "Adicionar"
4. **Teste imediatamente:** Clique "Testar"

### **Ações com credenciais:**

#### **🧪 Testar**
- **Função:** Verifica se credencial funciona
- **Processo:** Faz consulta de teste na API
- **Resultados possíveis:**
  - ✅ "Credenciais válidas e funcionando"
  - ❌ "Credenciais inválidas ou expiradas"
  - ⚠️ "Rate limit excedido"

#### **✏️ Editar**
- **Uso principal:** Atualizar token expirado
- **Processo:** Mantenha UUID, atualize apenas Token
- **Frequência:** A cada 30-90 dias

#### **🗑️ Excluir**
- **Quando usar:** Credencial permanentemente inválida
- **Cuidado:** Reduz capacidade de consultas
- **Confirmação:** Dupla verificação

### **Estratégia de múltiplas credenciais:**

**Para 3000+ clientes:**
- **Mínimo recomendado:** 5 credenciais
- **Capacidade total:** 300 consultas/minuto
- **Tempo para 3000 consultas:** ~10 minutos

**Dispositivos sugeridos:**
1. iPhone pessoal
2. iPad (se tiver)
3. Android pessoal/trabalho
4. Dispositivo de familiar
5. Tablet Android

## 🔔 SEÇÃO 4: Notificações

**Central de alertas e atividades do sistema.**

### **Tipos de notificação:**

#### **📊 Mudança de Status**
- **Quando:** Processo tem alteração detectada
- **Cor:** Azul
- **Prioridade:** Geralmente alta
- **Ação:** Verificar detalhes e notificar cliente

#### **✅ Sucesso**
- **Quando:** Operação concluída com êxito
- **Cor:** Verde
- **Exemplos:** Importação bem-sucedida, consulta manual
- **Ação:** Apenas informativo

#### **❌ Erro**
- **Quando:** Falha em operação
- **Cor:** Vermelho
- **Exemplos:** Credencial expirada, falha na API
- **Ação:** Corrigir problema indicado

#### **⚠️ Aviso**
- **Quando:** Situação que requer atenção
- **Cor:** Amarelo
- **Exemplos:** Rate limit, credencial expirando
- **Ação:** Tomar medida preventiva

#### **ℹ️ Informação**
- **Quando:** Relatórios e atualizações gerais
- **Cor:** Cinza
- **Exemplos:** Relatório diário, status do sistema
- **Ação:** Apenas acompanhar

### **Filtros disponíveis:**
- **Todas:** Mostra todas as notificações
- **Mudanças de Status:** Apenas alterações de processos
- **Erros:** Apenas problemas que precisam correção
- **Sucessos:** Apenas confirmações positivas
- **Avisos:** Apenas alertas preventivos
- **Informações:** Apenas relatórios gerais

### **Ações com notificações:**

#### **👁️ Marcar como Lida**
- **Função:** Remove destaque visual
- **Uso:** Após tomar conhecimento
- **Visual:** Notificação fica mais transparente

#### **🗑️ Excluir**
- **Função:** Remove notificação permanentemente
- **Uso:** Após resolver problema ou não ser mais relevante
- **Cuidado:** Não pode ser desfeito

#### **🧹 Limpar Todas**
- **Função:** Remove todas as notificações
- **Uso:** Limpeza geral periódica
- **Confirmação:** Dupla verificação

### **Interpretando notificações:**

**🔔 Notificação não lida:**
- Bolinha azul ao lado
- Texto em destaque
- Requer atenção

**👁️ Notificação lida:**
- Sem bolinha
- Texto mais claro
- Já foi vista

**📧 Informações do cliente:**
- Nome do cliente
- Número do processo
- Detalhes da mudança

## ⚙️ SEÇÃO 5: Configurações

**Personalize o comportamento da plataforma.**

### **📧 Notificações por E-mail:**

#### **Configurações:**
- **✅ Enviar notificações por e-mail**
  - **Função:** Ativa/desativa e-mails automáticos
  - **Recomendado:** Sempre ativo
  
- **📧 E-mail para Notificações**
  - **Função:** Define destinatário dos alertas
  - **Formato:** email@dominio.com
  - **Teste:** Botão "Testar" envia e-mail de verificação

#### **Quando você recebe e-mails:**
- 📊 **Mudanças detectadas** em processos
- ❌ **Erros críticos** do sistema
- 📋 **Relatório diário** de consultas
- ⚠️ **Alertas** de credenciais expirando

### **🕐 Agendamento de Consultas:**

#### **Configurações:**
- **✅ Executar consultas automáticas diariamente**
  - **Função:** Liga/desliga automação
  - **Recomendado:** Sempre ativo
  
- **⏰ Horário das Consultas**
  - **Padrão:** 08:00
  - **Formato:** 24 horas (HH:MM)
  - **Sugestão:** Horário que você verifica e-mails
  
- **📦 Tamanho do Lote**
  - **Padrão:** 10 consultas por vez
  - **Faixa:** 1-50
  - **Maior = mais rápido, mas mais chance de erro**

#### **🚀 Consulta Manual:**
- **Botão:** "Executar Consulta Manual"
- **Função:** Roda consultas imediatamente
- **Uso:** Testar sistema ou consulta urgente
- **Tempo:** Pode levar vários minutos

### **⚙️ Configurações Técnicas:**

#### **🔄 Máximo de Tentativas**
- **Padrão:** 3 tentativas
- **Função:** Quantas vezes tenta se falhar
- **Faixa:** 1-10
- **Maior = mais resiliente, mas mais lento**

#### **⏱️ Timeout (segundos)**
- **Padrão:** 30 segundos
- **Função:** Tempo limite para cada consulta
- **Faixa:** 10-120
- **Maior = mais tolerante, mas mais lento**

### **💾 Salvando configurações:**
1. **Altere os valores** desejados
2. **Clique:** "Salvar Configurações"
3. **Aguarde:** Confirmação "✅ Configurações salvas"
4. **Efeito:** Imediato para próximas operações

## 📈 OPERAÇÃO DIÁRIA

### **Rotina matinal recomendada:**

#### **1. Verificar Dashboard (2 minutos)**
- ✅ Status "Online"
- ✅ "Consultas Hoje" incrementou
- ✅ Verificar "Mudanças Detectadas"

#### **2. Revisar Notificações (5 minutos)**
- 📊 Mudanças de status → Verificar e notificar clientes
- ❌ Erros → Corrigir problemas
- ⚠️ Avisos → Tomar ações preventivas

#### **3. Acompanhar E-mails (automático)**
- 📧 Relatório diário chegará no seu e-mail
- 🔔 Alertas de mudanças importantes
- ⚠️ Avisos de problemas técnicos

### **Rotina semanal recomendada:**

#### **1. Revisar Credenciais (10 minutos)**
- 🧪 Testar todas as credenciais
- 📅 Verificar datas de último uso
- 🔄 Renovar se necessário

#### **2. Limpeza de Notificações (5 minutos)**
- 👁️ Marcar antigas como lidas
- 🗑️ Excluir irrelevantes
- 📊 Analisar padrões de mudanças

#### **3. Backup de Dados (5 minutos)**
- 💾 Exportar lista de clientes
- 🔐 Salvar credenciais em local seguro
- 📋 Documentar configurações importantes

### **Rotina mensal recomendada:**

#### **1. Análise de Performance (15 minutos)**
- 📊 Revisar estatísticas do mês
- 🔍 Identificar processos mais ativos
- 📈 Avaliar necessidade de mais credenciais

#### **2. Atualização de Credenciais (30 minutos)**
- 🔄 Renovar tokens que estão expirando
- 🆕 Adicionar novas credenciais se necessário
- 🧪 Testar todas as credenciais

#### **3. Manutenção de Clientes (20 minutos)**
- 📝 Atualizar informações de contato
- 🗑️ Remover clientes inativos
- 📊 Analisar padrões de mudanças

## 🚨 Solução de Problemas Comuns

### **Problema: Sistema mostra "Offline"**

**Possíveis causas:**
- Backend não está funcionando
- Problema de conectividade
- Manutenção do servidor

**Soluções:**
1. **Aguarde 5 minutos** e recarregue a página
2. **Verifique sua internet**
3. **Teste URL do backend** diretamente
4. **Contate suporte** se persistir

### **Problema: Nenhuma consulta hoje**

**Possíveis causas:**
- Agendamento desabilitado
- Todas as credenciais inválidas
- Erro no sistema de agendamento

**Soluções:**
1. **Verifique Configurações** → "Consultas automáticas diárias"
2. **Teste credenciais** na seção Credenciais
3. **Execute consulta manual** para testar
4. **Verifique notificações** por erros

### **Problema: Muitos erros 401 (Unauthorized)**

**Causa:** Credenciais expiraram

**Solução:**
1. **Vá em Credenciais**
2. **Teste cada uma** clicando "Testar"
3. **Renove tokens** das que falharam
4. **Use guia de credenciais** para extrair novos tokens

### **Problema: Rate limit excedido**

**Causa:** Muitas consultas muito rápido

**Soluções:**
1. **Adicione mais credenciais** para distribuir carga
2. **Aumente intervalo** entre consultas
3. **Reduza tamanho do lote** nas configurações
4. **Aguarde alguns minutos** antes de tentar novamente

### **Problema: Importação falha**

**Possíveis causas:**
- Formato de arquivo incorreto
- Dados obrigatórios faltando
- Processos duplicados

**Soluções:**
1. **Use template fornecido**
2. **Verifique campos obrigatórios** (Nome, Processo, Ano)
3. **Remova duplicatas** da planilha
4. **Tente lotes menores** (500 clientes por vez)

## 📊 Interpretando Relatórios

### **Relatório Diário (E-mail):**

**Seção de Estatísticas:**
- **Total de consultas:** Quantas foram feitas
- **Sucessos:** Consultas que funcionaram
- **Falhas:** Consultas que falharam
- **Mudanças detectadas:** Processos com alterações

**Interpretação:**
- **✅ Ideal:** 95%+ de sucessos, poucas falhas
- **⚠️ Atenção:** 80-95% sucessos, algumas falhas
- **🔴 Problema:** <80% sucessos, muitas falhas

**Seção de Mudanças:**
- **Lista de processos** que tiveram alterações
- **Tipo de mudança** detectada
- **Cliente afetado**

### **Dashboard de Estatísticas:**

**Tendências a observar:**
- **📈 Crescimento:** Mais clientes = mais consultas
- **🔄 Consistência:** Consultas diárias regulares
- **📊 Proporção:** Mudanças vs. total de consultas

**Alertas importantes:**
- **Queda súbita** em consultas → Problema técnico
- **Aumento em falhas** → Credenciais expirando
- **Muitas mudanças** → Período de alta atividade judicial

## 🎯 Otimização e Melhores Práticas

### **Para máxima eficiência:**

#### **Credenciais:**
- **Use 5+ credenciais** diferentes
- **Distribua entre dispositivos** (iPhone, Android, iPad)
- **Renove proativamente** antes de expirar
- **Mantenha backup** das credenciais

#### **Clientes:**
- **Organize por prioridade** (use campo Observações)
- **Mantenha dados atualizados** (email, telefone)
- **Use importação em lote** para grandes volumes
- **Remova clientes inativos** periodicamente

#### **Configurações:**
- **Horário de consulta:** Quando você verifica e-mails
- **E-mail sempre ativo** para não perder alertas
- **Tamanho de lote:** 10-20 para balancear velocidade/estabilidade
- **Timeout:** 30-60 segundos dependendo da conexão

### **Para máxima confiabilidade:**

#### **Monitoramento:**
- **Verifique dashboard** diariamente
- **Leia relatórios** por e-mail
- **Teste credenciais** semanalmente
- **Mantenha backup** dos dados

#### **Manutenção:**
- **Atualize credenciais** mensalmente
- **Limpe notificações** antigas
- **Revise configurações** periodicamente
- **Documente mudanças** importantes

## ✅ Checklist de Uso Diário

### **Manhã (5 minutos):**
- [ ] Abrir plataforma
- [ ] Verificar status "Online"
- [ ] Ver "Consultas Hoje" incrementou
- [ ] Revisar notificações novas
- [ ] Ler e-mail de relatório diário

### **Durante o dia (conforme necessário):**
- [ ] Verificar alertas de mudanças
- [ ] Notificar clientes sobre alterações importantes
- [ ] Adicionar novos clientes se necessário
- [ ] Responder a notificações de erro

### **Final do dia (2 minutos):**
- [ ] Marcar notificações como lidas
- [ ] Verificar se há erros pendentes
- [ ] Planejar ações para o próximo dia

### **Semanal (15 minutos):**
- [ ] Testar todas as credenciais
- [ ] Limpar notificações antigas
- [ ] Revisar configurações
- [ ] Fazer backup de dados importantes

### **Mensal (30 minutos):**
- [ ] Renovar credenciais expirando
- [ ] Analisar relatórios de performance
- [ ] Atualizar dados de clientes
- [ ] Otimizar configurações se necessário

## 🎉 Conclusão

Com este guia, você tem todas as informações necessárias para usar sua plataforma de automação de forma eficiente e confiável.

**Lembre-se:**
- ✅ **Consistência é chave** - Use diariamente
- ✅ **Monitore proativamente** - Não espere problemas
- ✅ **Mantenha atualizado** - Credenciais e dados
- ✅ **Documente mudanças** - Para referência futura

**Benefícios que você terá:**
- 🕐 **Economia de tempo** - Horas por dia
- 📊 **Melhor organização** - Tudo centralizado
- 🔔 **Nunca perde mudanças** - Alertas automáticos
- 📈 **Escala facilmente** - Milhares de processos
- 💼 **Mais profissional** - Clientes sempre informados

**Sua plataforma está trabalhando para você 24/7, consultando todos os processos e te alertando sobre qualquer mudança importante. Aproveite essa automação para focar no que realmente importa: atender melhor seus clientes!**

---

*Este guia cobre todas as funcionalidades da plataforma. Mantenha-o como referência e consulte sempre que tiver dúvidas sobre alguma operação.*

