# 🎲 RPG Manager — Gerenciador de Campanhas & Fichas

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Uma aplicação web completa desenvolvida com **Django** voltada para mestres e jogadores de RPG de mesa (TTRPG). O sistema permite gerenciar campanhas, vincular jogadores e controlar fichas de personagens com atributos complexos e cálculos automáticos de status.

</div>

---

## 📜 Sobre o Projeto

O **RPG Manager** foi idealizado para facilitar a organização de mesas de RPG, centralizando a gestão de campanhas e fichas em uma interface imersiva com temática *Dark Fantasy*. 

Inspirado em sistemas investigativos e narrativos de alta profundidade (com atributos como Intelecto, Psique, Físico, Habilidades Motoras e Parautilitário), o sistema automatiza as fórmulas matemáticas de recursos vitais (Estabilidade, Essência e Cansaço) de acordo com o nível e especialização de cada personagem.

---

## ✨ Funcionalidades Principais

### 🛡️ Gestão de Campanhas
- **Criação e Configuração**: O mestre pode definir o nome, sistema e descrição da campanha.
- **Vínculo de Jogadores**: Associação direta entre contas de usuários e a campanha (relação *Many-to-Many*).
- **Controle de Acesso**: Apenas o mestre criador tem permissão de edição e exclusão da campanha.

### 🧙‍♂️ Fichas de Personagem & Bestiário
- **Classificação Dinâmica**: Separação intuitiva entre **Jogadores**, **NPCs** e **Criaturas**.
- **Atributos Base (5 Pilares)**:
  - *Intelecto*, *Psique*, *Físico*, *Motoras* e *Parautilitário*.
- **Sistema Completo de Perícias**: Mais de 25 perícias distribuídas entre os atributos.
- **Cálculos Automáticos no Backend**:
  - **Estabilidade Máxima**: Calculada com base na Resistência e Físico.
  - **Essência Máxima**: Calculada com base no Parautilitário e Alma.
  - **Cansaço Máximo**: Calculado com base na Vontade e Psique.
- **Rastreamento em Tempo Real**: Monitoramento dos recursos atuais para controle durante as sessões.

### 🎨 Design & Experiência
- Interface totalmente responsiva estilizada com **CSS Customizado**.
- Identidade visual medieval/fantasia com tipografia **Cinzel** & **Inter** e paleta Dark & Gold.

---

## 🗂️ Estrutura do Projeto

```text
├── app/
│   ├── migrations/          # Histórico de migrações do banco
│   ├── templates/           # Telas HTML (Dashboard, Fichas, Campanhas, Login)
│   ├── admin.py             # Configuração do painel administrativo Django
│   ├── models.py            # Modelagem de dados (Campanha e Personagem)
│   ├── views.py             # Lógica de negócio e regras de controle
│   └── apps.py              # Configuração da aplicação
├── setup/
│   ├── settings.py          # Configurações do Django
│   ├── urls.py              # Mapeamento de rotas do projeto
│   ├── asgi.py & wsgi.py    # Pontos de entrada para servidores web
├── manage.py                # Utilitário de linha de comando do Django
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* **Python 3.10+** instalado na sua máquina
* **Git** instalado (opcional)

### Passo a passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Martinelli-Davi/rpg.git
   cd rpg
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # No Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # No Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **(Opcional) Crie um superusuário para acessar o Django Admin:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

7. Abra o navegador e acesse: `http://127.0.0.1:8000/`

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem**: [Python](https://www.python.org/)
* **Framework Web**: [Django](https://www.djangoproject.com/)
* **Banco de Dados**: [SQLite](https://www.sqlite.org/)
* **Frontend**: HTML5, CSS3, JavaScript
* **Fontes**: Google Fonts (Cinzel, Inter)

---

## 👤 Autor

Desenvolvido por **Davi Martinelli**.

- **GitHub**: [@Martinelli-Davi](https://github.com/Martinelli-Davi)
- **LinkedIn**: [Davi José](https://www.linkedin.com/in/davi-josé-472b66339)
- **E-mail**: [davijosemartinelle@gmail.com](mailto:davijosemartinelle@gmail.com)
