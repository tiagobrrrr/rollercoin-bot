# RollerCoin Automation Bot

Um bot de automação para RollerCoin com interface web para monitoramento e controle.

## Características

- ✅ Interface web responsiva com tema escuro
- ✅ Dashboard em tempo real com estatísticas
- ✅ Sistema de logs completo
- ✅ Controles start/stop do bot
- ✅ Configuração de credenciais
- ✅ Modo de simulação funcional
- ✅ Automação Selenium (em desenvolvimento)

## Instalação

1. **Instale Python 3.11+**

2. **Instale as dependências:**
```bash
pip install flask selenium webdriver-manager gunicorn requests
```

3. **Configure as variáveis de ambiente (opcional):**
```bash
export ROLLERCOIN_EMAIL="seu-email@exemplo.com"
export ROLLERCOIN_PASSWORD="sua-senha"
export CYCLE_INTERVAL=300
export SESSION_SECRET="sua-chave-secreta"
```

4. **Execute o bot:**
```bash
python main.py
```

5. **Acesse o dashboard:**
   - Abra http://localhost:5000 no seu navegador

## Estrutura do Projeto

```
rollercoin-bot/
├── main.py              # Aplicação Flask principal
├── bot.py               # Bot Selenium para RollerCoin
├── bot_simulator.py     # Simulador (modo atual)
├── config.py            # Configurações
├── templates/           # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── logs.html
├── static/              # CSS e JavaScript
│   ├── style.css
│   └── app.js
├── pyproject.toml       # Dependências
└── README.md           # Este arquivo
```

## Uso

### Dashboard Principal
- **Status do Bot**: Veja se está rodando ou parado
- **Estatísticas**: Total de execuções, erros, taxa de sucesso
- **Controles**: Botões para iniciar/parar o bot
- **Configuração**: Atualize email e senha do RollerCoin

### Logs
- Acesse a aba "Logs" para ver todas as atividades
- Auto-atualização a cada 10 segundos
- Códigos de cores para diferentes tipos de log

### API
- `GET /api/status` - Status atual do bot em JSON

## Configuração

### Credenciais do RollerCoin
1. Vá para o dashboard
2. Scroll até a seção "Configuration"
3. Digite seu email e senha do RollerCoin
4. Clique em "Update Configuration"

### Variáveis de Ambiente
- `ROLLERCOIN_EMAIL` - Seu email do RollerCoin
- `ROLLERCOIN_PASSWORD` - Sua senha do RollerCoin
- `CYCLE_INTERVAL` - Intervalo entre ciclos em segundos (padrão: 300)
- `SESSION_SECRET` - Chave secreta para sessões Flask
- `DEBUG` - Modo debug (True/False)

## Modo Atual: Simulação

O bot está executando em **modo de simulação** que demonstra toda a funcionalidade:
- Login simulado no RollerCoin
- Coleta de recompensas simulada
- Mini-jogos simulados
- Logs realistas de atividades

### Ativando o Selenium Real
Para usar automação real do browser:
1. Instale Chrome/Chromium
2. No arquivo `main.py`, linha 56, troque:
   ```python
   bot = RollerCoinBotSimulator()
   ```
   por:
   ```python
   bot = RollerCoinBot()
   ```

## Funcionalidades do Bot

### Automação RollerCoin
- Login automático
- Coleta de recompensas diárias
- Execução de mini-jogos
- Verificação de status de mineração
- Atualização de equipamentos

### Monitoramento
- Status em tempo real
- Contadores de execuções
- Taxa de sucesso
- Logs detalhados
- Tratamento de erros

### Segurança
- Credenciais via variáveis de ambiente
- Sessões seguras Flask
- Modo headless do browser
- Tratamento robusto de erros

## Requisitos do Sistema

- Python 3.11+
- Chrome/Chromium (para Selenium)
- 512MB+ RAM
- Conexão com internet

## Suporte

Este bot foi desenvolvido para demonstração e uso educacional. 
Para suporte, consulte os logs em tempo real no dashboard.

## Status de Desenvolvimento

- ✅ Interface web completa
- ✅ Sistema de logs
- ✅ Simulador funcional
- 🔄 Selenium em desenvolvimento (problemas de compatibilidade resolvidos)
- ✅ Dashboard responsivo

---

**Desenvolvido em 2025 - Bot de Automação RollerCoin**"# rollercoin-bot"  
"# rollercoin-bot" 
