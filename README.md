# 🌴 SmartReader

SmartReader é um assistente de leitura inteligente que identifica livros por imagem ou texto e oferece análises detalhadas.

#### ⚙️ Funcionalidades

##### 1. Identificação de Livros
- 📁 Upload de arquivo (JPG, JPEG, PNG)
- 📸 Captura de foto via câmera
- ✍️ Busca por título e autor

##### 2. Análise Detalhada
- 📌 Sobre a obra
- 📜 Resumo do conteúdo
- 💡 Principais conceitos
- 🔗 Obras relacionadas
- 👤 Informações do autor
- 📍 Onde encontrar

#### 🚀 Como Usar

1. Acesse a aplicação: [SmartReader](https://redaertrams.streamlit.app/)
2. Escolha o método de entrada
3. Explore as informações disponíveis sobre o livro

#### 🛠️ Tecnologias

- Python
- Streamlit
- Google Gemini AI

#### ⚙️ Instalação Local

1. Clone o repositório
```bash
git clone https://github.com/domafras/smartreader.git
cd smartreader
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
- Crie um arquivo `.streamlit/secrets.toml`
- Adicione sua chave API do Google Gemini:
```toml
GEMINI_CHAVE = "sua-chave-aqui"
```

5. Execute a aplicação
```bash
streamlit run main.py
``` 

#### ✏️ Sobre

- Esse projeto foi desenvolvido com orientação do Professor Doutor Marcos Oliveira durante curso de extensão da UFPR.

#### 👨‍💻 Contatos

- [LinkedIn](https://www.linkedin.com/in/leomafra/)
- [GitHub](https://github.com/domafras)
- [Medium](https://domafras.medium.com/)
