# 🚀 Guia Completo de Deploy - Plataforma Giustizia Civile

**Para usuários SEM conhecimento técnico**

Este guia vai te ensinar como colocar sua plataforma online usando ferramentas **100% GRATUITAS**. Você não precisa saber programação - apenas seguir os passos!

## 📋 O que você vai conseguir

Ao final deste guia, você terá:
- ✅ **Frontend online** - Interface da plataforma acessível por qualquer navegador
- ✅ **Backend funcionando** - Servidor processando todas as consultas
- ✅ **Integração completa** - Sistema funcionando automaticamente
- ✅ **URLs permanentes** - Links que nunca mudam
- ✅ **Atualizações fáceis** - Como atualizar quando necessário

## 🛠️ Ferramentas que vamos usar (TODAS GRATUITAS)

### **1. GitHub** - Para armazenar o código
- **Custo:** Gratuito
- **Limite:** Ilimitado para projetos públicos
- **Por que usar:** Necessário para as outras ferramentas

### **2. Vercel** - Para o Frontend (Interface)
- **Custo:** Gratuito
- **Limite:** 100GB de banda por mês
- **Por que usar:** Muito fácil de usar, deploy automático

### **3. Railway** - Para o Backend (Servidor)
- **Custo:** Gratuito
- **Limite:** $5 de crédito por mês (suficiente para uso normal)
- **Por que usar:** Suporta Python, banco de dados incluído

## 📚 PARTE 1: Preparando o GitHub

### **Passo 1.1: Criar conta no GitHub**

1. **Acesse:** https://github.com
2. **Clique em "Sign up"**
3. **Preencha:**
   - Username: `seu-nome-giustizia` (exemplo)
   - Email: seu e-mail
   - Password: senha forte
4. **Confirme o e-mail** que o GitHub enviar

### **Passo 1.2: Criar repositório**

1. **Clique no "+" no canto superior direito**
2. **Selecione "New repository"**
3. **Preencha:**
   - Repository name: `giustizia-platform`
   - Description: `Plataforma de Automação Giustizia Civile`
   - ✅ Marque "Public"
   - ✅ Marque "Add a README file"
4. **Clique "Create repository"**

### **Passo 1.3: Fazer upload dos arquivos**

**Opção A: Upload via interface (MAIS FÁCIL)**

1. **Na página do seu repositório, clique "uploading an existing file"**
2. **Arraste TODA a pasta `giustizia-platform-complete`**
3. **Aguarde o upload (pode demorar alguns minutos)**
4. **Na parte inferior:**
   - Commit message: `Primeira versão da plataforma`
   - ✅ Marque "Commit directly to the main branch"
5. **Clique "Commit changes"**

**Opção B: GitHub Desktop (SE PREFERIR)**

1. **Baixe GitHub Desktop:** https://desktop.github.com
2. **Instale e faça login**
3. **Clone seu repositório**
4. **Copie os arquivos para a pasta local**
5. **Commit e push**

## 🎨 PARTE 2: Deploy do Frontend (Vercel)

### **Passo 2.1: Criar conta no Vercel**

1. **Acesse:** https://vercel.com
2. **Clique "Sign Up"**
3. **Escolha "Continue with GitHub"**
4. **Autorize o Vercel** a acessar seus repositórios

### **Passo 2.2: Fazer deploy do frontend**

1. **No dashboard do Vercel, clique "New Project"**
2. **Encontre seu repositório `giustizia-platform`**
3. **Clique "Import"**
4. **Configure o projeto:**
   - Project Name: `giustizia-frontend`
   - Framework Preset: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
5. **Clique "Deploy"**

### **Passo 2.3: Aguardar deploy**

- ⏱️ **Tempo:** 2-5 minutos
- 📊 **Progresso:** Você verá logs em tempo real
- ✅ **Sucesso:** Aparecerá uma URL como `https://giustizia-frontend-abc123.vercel.app`

### **Passo 2.4: Testar frontend**

1. **Clique na URL gerada**
2. **Você deve ver:** Interface da plataforma carregando
3. **Status esperado:** "Sistema Offline" (normal, backend ainda não está online)

## 🔧 PARTE 3: Deploy do Backend (Railway)

### **Passo 3.1: Criar conta no Railway**

1. **Acesse:** https://railway.app
2. **Clique "Login"**
3. **Escolha "Login with GitHub"**
4. **Autorize o Railway**

### **Passo 3.2: Criar projeto**

1. **No dashboard, clique "New Project"**
2. **Selecione "Deploy from GitHub repo"**
3. **Escolha seu repositório `giustizia-platform`**
4. **Clique "Deploy Now"**

### **Passo 3.3: Configurar o backend**

1. **Após o deploy inicial, clique no projeto**
2. **Clique na aba "Settings"**
3. **Em "Environment", adicione:**
   - `PYTHONPATH`: `src`
   - `PORT`: `8000`
4. **Em "Deploy", configure:**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src && python main.py`

### **Passo 3.4: Aguardar deploy**

- ⏱️ **Tempo:** 3-7 minutos
- 📊 **Progresso:** Logs aparecem em tempo real
- ✅ **Sucesso:** Status muda para "Active"
- 🌐 **URL:** Algo como `https://giustizia-backend-production.up.railway.app`

### **Passo 3.5: Testar backend**

1. **Copie a URL do backend**
2. **Adicione `/api/health` no final**
3. **Exemplo:** `https://giustizia-backend-production.up.railway.app/api/health`
4. **Acesse no navegador**
5. **Deve aparecer:** `{"status": "online", "timestamp": "...", "version": "1.0.0"}`

## 🔗 PARTE 4: Conectar Frontend e Backend

### **Passo 4.1: Configurar URL do backend no frontend**

1. **Volte ao Vercel**
2. **Vá no seu projeto do frontend**
3. **Clique em "Settings"**
4. **Clique em "Environment Variables"**
5. **Adicione nova variável:**
   - Name: `REACT_APP_API_URL`
   - Value: `https://giustizia-backend-production.up.railway.app` (sua URL do Railway)
   - Environment: `Production`
6. **Clique "Save"**

### **Passo 4.2: Fazer redeploy do frontend**

1. **Vá na aba "Deployments"**
2. **Clique nos "..." do último deploy**
3. **Selecione "Redeploy"**
4. **Aguarde 2-3 minutos**

### **Passo 4.3: Testar integração completa**

1. **Acesse sua URL do frontend**
2. **Aguarde carregar**
3. **Status deve mostrar:** "Sistema Online" ✅
4. **Dashboard deve mostrar:** Números reais (mesmo que zerados)

## ✅ PARTE 5: Verificação Final

### **Checklist de funcionamento:**

- [ ] **Frontend carrega** sem erros
- [ ] **Status mostra "Online"** (bolinha verde)
- [ ] **Consegue navegar** entre as seções
- [ ] **Seção Clientes** abre normalmente
- [ ] **Seção Credenciais** abre normalmente
- [ ] **Botão "Adicionar Cliente"** abre modal
- [ ] **Botão "Adicionar Credencial"** abre modal

### **Se algo não funcionar:**

1. **Verifique as URLs:**
   - Frontend: Deve carregar a interface
   - Backend + `/api/health`: Deve mostrar JSON com status

2. **Verifique variáveis de ambiente:**
   - No Vercel: `REACT_APP_API_URL` deve ter a URL do Railway
   - No Railway: `PYTHONPATH` deve ser `src`

3. **Verifique logs:**
   - Vercel: Aba "Functions" → Ver logs
   - Railway: Aba "Deployments" → Ver logs

## 🎯 PARTE 6: Usando a Plataforma

### **Passo 6.1: Adicionar suas credenciais**

1. **Acesse a seção "Credenciais"**
2. **Clique "Adicionar Credencial"**
3. **Preencha:**
   - Nome: "Meu iPhone" (ou identificador)
   - UUID: (extraído do app - veja guia de credenciais)
   - Token: (extraído do app - veja guia de credenciais)
   - Dispositivo: Selecione o tipo
4. **Clique "Adicionar"**
5. **Teste a credencial** clicando em "Testar"

### **Passo 6.2: Adicionar clientes**

**Opção A: Um por vez**
1. **Vá em "Clientes"**
2. **Clique "Adicionar Cliente"**
3. **Preencha os dados**
4. **Clique "Adicionar"**

**Opção B: Importação em lote**
1. **Clique "Importar Lote"**
2. **Baixe o template CSV**
3. **Preencha com seus dados**
4. **Faça upload do arquivo**

### **Passo 6.3: Configurar notificações**

1. **Vá em "Configurações"**
2. **Configure:**
   - ✅ Enviar notificações por email
   - Email: seu-email@gmail.com
   - ✅ Consultas automáticas diárias
   - Horário: 08:00 (ou preferido)
3. **Clique "Salvar Configurações"**

## 🔄 PARTE 7: Atualizações e Manutenção

### **Como atualizar a plataforma:**

1. **Baixe nova versão** dos códigos
2. **No GitHub:**
   - Substitua os arquivos antigos
   - Commit as mudanças
3. **Deploy automático:**
   - Vercel: Atualiza automaticamente
   - Railway: Atualiza automaticamente

### **Monitoramento:**

- **Vercel Analytics:** Veja quantas pessoas acessam
- **Railway Metrics:** Monitore uso do servidor
- **Logs:** Sempre disponíveis para debug

### **Backup:**

- **Código:** Sempre no GitHub
- **Banco de dados:** Railway faz backup automático
- **Configurações:** Salvas no banco

## 🆘 PARTE 8: Solução de Problemas

### **Problema: Frontend não carrega**

**Possíveis causas:**
- Build falhou no Vercel
- Erro no código React
- Variável de ambiente incorreta

**Soluções:**
1. Vá no Vercel → Deployments → Ver logs
2. Procure por erros em vermelho
3. Se erro de build: Verifique se todos os arquivos foram enviados
4. Se erro de variável: Verifique `REACT_APP_API_URL`

### **Problema: Backend não responde**

**Possíveis causas:**
- Deploy falhou no Railway
- Erro no código Python
- Dependências não instaladas

**Soluções:**
1. Vá no Railway → Deployments → Ver logs
2. Procure por erros em vermelho
3. Se erro de dependência: Verifique `requirements.txt`
4. Se erro de código: Verifique se todos os arquivos estão na pasta `src`

### **Problema: "Sistema Offline"**

**Possíveis causas:**
- Backend não está rodando
- URL do backend incorreta no frontend
- Problema de CORS

**Soluções:**
1. Teste `sua-url-backend/api/health` no navegador
2. Se não funcionar: Problema no backend (ver acima)
3. Se funcionar: Problema na conexão frontend-backend
4. Verifique variável `REACT_APP_API_URL` no Vercel

### **Problema: Credenciais não funcionam**

**Possíveis causas:**
- UUID ou Token incorretos
- Credenciais expiraram
- Rate limit da API

**Soluções:**
1. Re-extraia as credenciais do app
2. Teste com processo conhecido
3. Use múltiplas credenciais
4. Aguarde alguns minutos entre testes

## 📞 PARTE 9: Suporte e Recursos

### **Documentação oficial:**

- **Vercel:** https://vercel.com/docs
- **Railway:** https://docs.railway.app
- **GitHub:** https://docs.github.com

### **Comunidades de ajuda:**

- **Stack Overflow:** Para erros técnicos
- **GitHub Issues:** Para problemas específicos
- **Discord/Telegram:** Comunidades de desenvolvedores

### **Monitoramento de custos:**

- **Vercel:** Dashboard → Usage
- **Railway:** Dashboard → Usage
- **GitHub:** Sempre gratuito para projetos públicos

## 🎉 Parabéns!

Se você chegou até aqui e tudo está funcionando, você conseguiu:

✅ **Colocar uma plataforma completa online**
✅ **Integrar frontend e backend**
✅ **Configurar automação de consultas**
✅ **Criar um sistema profissional**

Sua plataforma agora está:
- 🌐 **Online 24/7**
- 🔄 **Atualizando automaticamente**
- 📧 **Enviando notificações**
- 📊 **Monitorando processos**

**URLs finais:**
- **Frontend:** `https://seu-projeto.vercel.app`
- **Backend:** `https://seu-projeto.up.railway.app`

**Próximos passos:**
1. Adicione todos os seus clientes
2. Configure múltiplas credenciais
3. Teste o sistema por alguns dias
4. Ajuste configurações conforme necessário

**Lembre-se:** Sua plataforma está rodando em serviços profissionais e confiáveis. Ela vai funcionar automaticamente todos os dias às 8:00 da manhã, consultando todos os seus processos e te notificando sobre qualquer mudança!

---

*Este guia foi criado para ser seguido por qualquer pessoa, mesmo sem conhecimento técnico. Se você teve alguma dificuldade, revise os passos ou procure ajuda nas comunidades mencionadas.*

