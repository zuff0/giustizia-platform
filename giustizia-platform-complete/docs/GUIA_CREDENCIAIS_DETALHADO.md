# 🔑 Guia Completo: Como Obter UUID e Token da Giustizia Civile

**Para usuários SEM conhecimento técnico**

Este guia vai te ensinar como extrair as credenciais necessárias do aplicativo oficial da Giustizia Civile para usar na sua plataforma de automação.

## 📱 O que são UUID e Token?

### **UUID (Identificador Único)**
- **O que é:** Um código que identifica seu dispositivo
- **Formato:** `550e8400-e29b-41d4-a716-446655440000`
- **Função:** Diz para a API qual dispositivo está fazendo a consulta
- **Permanência:** Geralmente não muda (mesmo dispositivo)

### **Token (Chave de Autenticação)**
- **O que é:** Uma "senha" temporária que prova que você tem acesso
- **Formato:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (muito longo)
- **Função:** Autoriza suas consultas na API oficial
- **Permanência:** Expira periodicamente (30-90 dias)

## 🎯 Método Recomendado: Charles Proxy

**Este é o método mais confiável e funciona tanto no iPhone quanto no Android.**

### **Passo 1: Preparar o computador**

#### **1.1: Baixar Charles Proxy**
1. **Acesse:** https://www.charlesproxy.com/download/
2. **Baixe a versão** para seu sistema (Windows/Mac)
3. **Instale normalmente** (pode usar a versão trial de 30 dias)
4. **Abra o Charles Proxy**

#### **1.2: Configurar HTTPS**
1. **No Charles, vá em:** `Proxy` → `SSL Proxying Settings`
2. **Marque:** ✅ `Enable SSL Proxying`
3. **Clique:** `Add`
4. **Preencha:**
   - Host: `*` (asterisco)
   - Port: `443`
5. **Clique:** `OK` → `OK`

#### **1.3: Descobrir IP do computador**

**No Windows:**
1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter
3. Digite `ipconfig` e pressione Enter
4. Procure por "Endereço IPv4" (algo como `192.168.1.100`)
5. **Anote este IP**

**No Mac:**
1. Vá em `System Preferences` → `Network`
2. Selecione sua conexão Wi-Fi
3. O IP aparece do lado direito (ex: `192.168.1.100`)
4. **Anote este IP**

### **Passo 2: Configurar o celular**

#### **2.1: Conectar na mesma rede Wi-Fi**
- **Importante:** Celular e computador devem estar na **mesma rede Wi-Fi**

#### **2.2: Configurar proxy no iPhone**
1. **Vá em:** `Configurações` → `Wi-Fi`
2. **Toque no (i)** ao lado da rede conectada
3. **Role para baixo** até "Proxy HTTP"
4. **Selecione:** `Manual`
5. **Preencha:**
   - Servidor: `192.168.1.100` (o IP que você anotou)
   - Porta: `8888`
6. **Toque:** `Salvar`

#### **2.3: Configurar proxy no Android**
1. **Vá em:** `Configurações` → `Wi-Fi`
2. **Toque e segure** na rede conectada
3. **Selecione:** `Modificar rede`
4. **Toque:** `Opções avançadas`
5. **Em Proxy, selecione:** `Manual`
6. **Preencha:**
   - Nome do host do proxy: `192.168.1.100` (o IP que você anotou)
   - Porta do proxy: `8888`
7. **Toque:** `Salvar`

### **Passo 3: Instalar certificado SSL**

#### **3.1: Baixar certificado**
1. **No celular, abra o navegador** (Safari no iPhone, Chrome no Android)
2. **Acesse:** `chls.pro/ssl`
3. **Baixe o certificado** quando solicitado

#### **3.2: Instalar no iPhone**
1. **Vá em:** `Configurações` → `Geral` → `Perfis e Gerenciamento de Dispositivo`
2. **Toque no perfil** "Charles Proxy CA"
3. **Toque:** `Instalar` → `Instalar` → `Instalar`
4. **Agora vá em:** `Configurações` → `Geral` → `Sobre`
5. **Role até o final** e toque em `Configurações de Confiança do Certificado`
6. **Ative o switch** para "Charles Proxy CA" ✅

#### **3.3: Instalar no Android**
1. **Vá em:** `Configurações` → `Segurança` → `Credenciais`
2. **Toque:** `Instalar do armazenamento`
3. **Selecione o arquivo** baixado
4. **Digite sua senha/PIN** se solicitado
5. **Dê um nome** ao certificado (ex: "Charles")
6. **Toque:** `OK`

### **Passo 4: Capturar as credenciais**

#### **4.1: Iniciar captura**
1. **No Charles Proxy (computador):**
   - Clique no ícone de "vassoura" para limpar
   - Clique no botão "Record" (deve ficar vermelho)

#### **4.2: Usar o app Giustizia Civile**
1. **No celular, abra o app** Giustizia Civile
2. **Faça login** normalmente
3. **Realize uma consulta** de qualquer processo
4. **Aguarde a consulta** terminar (sucesso ou falha, não importa)

#### **4.3: Parar captura**
1. **No Charles, clique** no botão "Record" para parar

#### **4.4: Encontrar as credenciais**
1. **No Charles, procure por:** `mob.processotelematico.giustizia.it`
2. **Expanda a pasta** clicando na setinha
3. **Procure por:** `proxy`
4. **Clique em:** `index_mobile` (requisição POST)
5. **Na parte inferior, clique na aba:** `Request`
6. **Clique na sub-aba:** `Headers`

#### **4.5: Extrair UUID e Token**
**Procure por estas linhas nos headers:**

```
uuid: 550e8400-e29b-41d4-a716-446655440000
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Ou pode aparecer como:**
```
device-id: 550e8400-e29b-41d4-a716-446655440000
authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Copie estes valores:**
- **UUID:** O código de 36 caracteres com hífens
- **Token:** O código longo que começa com "eyJ" (pode ter centenas de caracteres)

### **Passo 5: Limpar configurações**

#### **5.1: Remover proxy do celular**

**iPhone:**
1. `Configurações` → `Wi-Fi`
2. Toque no (i) da rede
3. Em "Proxy HTTP" selecione: `Off`

**Android:**
1. `Configurações` → `Wi-Fi`
2. Toque e segure na rede → `Modificar rede`
3. `Opções avançadas` → Proxy: `Nenhum`

#### **5.2: Manter certificado (opcional)**
- **Pode deixar instalado** para futuras extrações
- **Para remover:** Siga o processo inverso da instalação

## 🔄 Método Alternativo: Logs do Android (Avançado)

**Este método funciona apenas no Android e requer conhecimento técnico.**

### **Pré-requisitos:**
- Celular Android
- Cabo USB
- Computador com Windows/Mac/Linux
- Depuração USB habilitada

### **Passo 1: Habilitar Depuração USB**
1. **Vá em:** `Configurações` → `Sobre o telefone`
2. **Toque 7 vezes** em "Número da versão"
3. **Volte para Configurações** → `Opções do desenvolvedor`
4. **Ative:** ✅ `Depuração USB`

### **Passo 2: Instalar ADB**
1. **Baixe Android SDK Platform Tools**
2. **Extraia em uma pasta** (ex: `C:\adb`)
3. **Abra terminal/prompt** nesta pasta

### **Passo 3: Conectar celular**
1. **Conecte via USB**
2. **No terminal, digite:** `adb devices`
3. **Autorize no celular** se aparecer popup
4. **Deve aparecer:** `device` na lista

### **Passo 4: Capturar logs**
1. **Digite:** `adb logcat > logs.txt`
2. **No celular, abra** Giustizia Civile
3. **Faça uma consulta**
4. **Pressione Ctrl+C** para parar
5. **Abra logs.txt** e procure por "uuid" e "token"

## 🛠️ Método para Múltiplas Credenciais

**Para aumentar a capacidade de consultas, você pode extrair credenciais de múltiplos dispositivos.**

### **Estratégia recomendada:**
1. **iPhone pessoal** - Credencial 1
2. **iPad** (se tiver) - Credencial 2
3. **Android** (se tiver) - Credencial 3
4. **Celular de familiar** - Credencial 4
5. **Tablet Android** - Credencial 5

### **Benefícios:**
- **60 consultas/minuto** por credencial
- **5 credenciais = 300 consultas/minuto**
- **Suficiente para 3000+ clientes** em poucas horas

### **Processo:**
1. **Instale o app** em cada dispositivo
2. **Faça login** com a mesma conta
3. **Extraia credenciais** de cada um usando Charles
4. **Adicione todas** na plataforma

## ⚠️ Problemas Comuns e Soluções

### **Problema: Não aparece tráfego no Charles**

**Possíveis causas:**
- IP do computador incorreto
- Proxy não configurado no celular
- Firewall bloqueando

**Soluções:**
1. **Verifique o IP** novamente
2. **Desative firewall** temporariamente
3. **Teste acessando** google.com no celular
4. **Deve aparecer tráfego** no Charles

### **Problema: HTTPS não funciona**

**Possíveis causas:**
- Certificado não instalado
- Certificado não confiável
- SSL Proxying não habilitado

**Soluções:**
1. **Reinstale o certificado**
2. **Verifique se está marcado como confiável**
3. **Confirme SSL Proxying** no Charles

### **Problema: App não conecta**

**Possíveis causas:**
- Proxy interferindo na conexão
- Certificado causando problemas
- App detectando proxy

**Soluções:**
1. **Teste sem proxy** primeiro
2. **Verifique se app funciona** normalmente
3. **Depois configure proxy** novamente

### **Problema: Não encontro UUID/Token**

**Possíveis causas:**
- Consulta não foi feita
- Tráfego não capturado
- Headers em local diferente

**Soluções:**
1. **Faça nova consulta** no app
2. **Procure por outras URLs** da Giustizia
3. **Verifique aba "Response"** também
4. **Procure por "authorization"** ou "bearer"

### **Problema: Token muito longo**

**Isso é normal!** Tokens JWT podem ter 500+ caracteres.

**Como copiar:**
1. **Clique triplo** para selecionar tudo
2. **Ctrl+C** para copiar
3. **Cole em arquivo de texto** para verificar
4. **Copie completo** para a plataforma

## 🔒 Segurança e Boas Práticas

### **Proteção das credenciais:**
- ✅ **Nunca compartilhe** UUID e Token
- ✅ **Use apenas em sua plataforma**
- ✅ **Mantenha backup** em local seguro
- ✅ **Renove periodicamente** (30-90 dias)

### **Monitoramento:**
- 📊 **Acompanhe uso** na plataforma
- ⚠️ **Fique atento a erros** 401 (token expirado)
- 🔄 **Tenha múltiplas credenciais** como backup

### **Renovação:**
- 📅 **Marque no calendário** para renovar
- 🔔 **Configure alertas** na plataforma
- 🚀 **Processo fica mais rápido** com prática

## 📊 Testando as Credenciais

### **Na plataforma:**
1. **Vá em "Credenciais"**
2. **Clique "Adicionar Credencial"**
3. **Preencha:**
   - Nome: "iPhone Principal"
   - UUID: (cole o valor extraído)
   - Token: (cole o valor extraído)
   - Dispositivo: iPhone
4. **Clique "Adicionar"**
5. **Clique "Testar"**

### **Resultados esperados:**
- ✅ **Sucesso:** "Credenciais válidas e funcionando"
- ❌ **Falha:** "Credenciais inválidas ou expiradas"
- ⚠️ **Rate limit:** "Tente novamente mais tarde"

## 🎯 Dicas Avançadas

### **Para usuários experientes:**

#### **Automatizar extração:**
- Use scripts Python com `mitmproxy`
- Configure interceptação automática
- Salve credenciais em arquivo JSON

#### **Monitorar expiração:**
- Implemente verificação diária
- Configure alertas automáticos
- Renove proativamente

#### **Otimizar performance:**
- Distribua consultas entre credenciais
- Implemente cache inteligente
- Use rate limiting adaptativo

## 🆘 Suporte e Ajuda

### **Se nada funcionar:**

1. **Revise cada passo** cuidadosamente
2. **Teste com dispositivo diferente**
3. **Procure ajuda** em comunidades técnicas
4. **Considere contratar** um técnico

### **Recursos úteis:**
- **Charles Proxy Docs:** https://www.charlesproxy.com/documentation/
- **Android ADB Guide:** https://developer.android.com/studio/command-line/adb
- **Comunidades:** Stack Overflow, Reddit r/androiddev

## ✅ Checklist Final

Antes de usar as credenciais na plataforma:

- [ ] **UUID extraído** (36 caracteres com hífens)
- [ ] **Token extraído** (centenas de caracteres)
- [ ] **Credenciais testadas** na plataforma
- [ ] **Proxy removido** do celular
- [ ] **App funciona** normalmente
- [ ] **Backup das credenciais** salvo

## 🎉 Parabéns!

Se você conseguiu extrair as credenciais, você:

✅ **Dominou um processo técnico complexo**
✅ **Tem acesso à API oficial**
✅ **Pode automatizar milhares de consultas**
✅ **Economizará horas de trabalho manual**

**Próximos passos:**
1. Configure as credenciais na plataforma
2. Adicione seus clientes
3. Teste com poucos processos primeiro
4. Configure consultas automáticas
5. Monitore e ajuste conforme necessário

**Lembre-se:** Este processo pode parecer complicado na primeira vez, mas fica muito mais fácil com a prática. Suas credenciais são a chave para automatizar completamente o monitoramento dos seus processos!

---

*Este guia foi criado para ser o mais detalhado possível. Se você teve dificuldades, não desista - o resultado vale muito a pena!*

