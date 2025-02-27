import streamlit as st
from PIL import Image
import inteligencia

# Configuração inicial do modelo
inteligencia.configurar_gemini(st.secrets["GEMINI_CHAVE"])

# Configuração inicial da página
st.set_page_config(
    layout='wide',
    page_title="SmartReader",
    page_icon="🌴",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/leomafra/',
        'Report a bug': 'https://github.com/domafras/smartreader',
        'About': 'SmartReader é um projeto desenvolvido durante curso de extensão na UFPR que serve como assistente de leitura inteligente baseado na Gemini AI.'
    }
)

# Logo (ícone)
st.logo(image="assets/logo.svg",
        size="medium",
        link="https://www.linkedin.com/in/leomafra/")

# Centralização e margem
st.html(
    """
    <style>
    h1.centered {
        text-align: center;
        margin-top: 0px;
        margin-bottom: 0px;
        font-size: 2.75em;
        line-height: 1;
        color: #33C363;
    }
    p.centered {
        text-align: center;
        margin-top: -15px;
        margin-bottom: -10px;
        font-size: 1em;
        line-height: 1.5; 
    }
    </style>
    """
)

# Cabeçalho estilizado
st.html('<h1 class="centered">SmartReader</h1>')
st.html('<p class="centered">O seu assistente de leitura inteligente.</p>')

# Linha separadora
st.divider()

# Área principal
col_esq, col_dir = st.columns([1, 1], gap="large")

# Coluna da esquerda
with col_esq:
    st.markdown("##### 1. Identificar Livro")
    
    # Seletor de método de entrada
    opcoes = {
        "Arquivo": "📁 Arquivo",
        "Câmera": "📸 Câmera",
        "Texto": "✍️ Texto"
    }
    opcao_entrada = st.radio("Selecione o método de envio:",
                             options=opcoes.keys(), 
                             format_func=lambda x: opcoes[x], 
                             horizontal=True)

    # Opção de imagem (Arquivo ou Câmera)
    if opcao_entrada in ["Arquivo", "Câmera"]:
        entrada_imagem = (
            st.file_uploader("Arraste ou selecione um arquivo", type=["jpg", "jpeg", "png"])
            if opcao_entrada == "Arquivo"
            else st.camera_input("Tire uma foto:")
        )

        # Se houver uma imagem enviada
        if entrada_imagem is not None:
            img = Image.open(entrada_imagem)
            with st.expander("Pré-visualização da capa", expanded=True):
                st.image(img, width=200)
                
            if st.button("👁️ Inspecionar", use_container_width=True):
                with st.spinner("Analisando livro..."):
                    st.session_state.livro = inteligencia.inspecionar_livro(img)
    
    # Opção de pesquisa (Texto)
    else: 
        with st.form("form_pesquisa_texto"):
            titulo = st.text_input("Título do livro", 
                                 placeholder="Digite o título do livro",
                                 help="Exemplo: 'Memórias Póstumas de Brás Cubas'")
            autor = st.text_input("Autor", 
                                placeholder="Digite o nome do autor",
                                help="Exemplo: 'Machado de Assis'")
            
            pesquisar = st.form_submit_button("👁️ Pesquisar", use_container_width=True)
            
            # Processar pesquisa quando formulário enviado
            if pesquisar:
                if not titulo.strip() or not autor.strip():
                    st.error("Preencha o título e autor do livro corretamente.")
                else:
                    with st.spinner("Buscando informações do livro..."):
                        # Criar objeto livro com dados informados
                        livro_temp = {
                            'Título': titulo,
                            'Autor': autor
                        }
                        
                        # Verificar existência do livro
                        resultado = inteligencia.pesquisar_livro(livro_temp, 'Sobre')
                        
                        # Salvar na sessão (seja livro válido ou erro)
                        tem_erro = isinstance(resultado, dict) and 'erro' in resultado
                        st.session_state.livro = resultado if tem_erro else livro_temp

    # Exibição dos detalhes do livro
    if 'livro' in st.session_state:
        livro = st.session_state.livro
        if 'erro' in livro:
            st.error(livro['erro'])
        else:
            with st.container():
                st.header(f":green[{livro.get('Título', '')}]")
                
                if 'Subtítulo' in livro:
                    st.markdown(f"#### *{livro['Subtítulo']}*")
                
                st.markdown("Detalhes:")
                for chave, valor in livro.items():
                    if chave not in ['Título', 'Subtítulo']:
                        st.markdown(f"- **{chave}:** {valor}")

# Coluna da direita
with col_dir:
    if 'livro' in st.session_state and 'erro' not in st.session_state.livro:
        st.markdown("##### 2. Explorar Detalhes")
        
        opcao_info = {
            'Sobre': '📌 Sobre',
            'Resumo': '📜 Resumo',
            'Conceitos': '💡 Conceitos',
            'Obras relacionadas': '🔗 Obras relacionadas',
            'Mais do autor': '👤 Mais do autor',
            'Onde encontrar': '📍 Onde encontrar'
        }
        
        with st.container():
            selecao = st.selectbox("Selecione o tipo de conteúdo:",
                                   list(opcao_info.keys()),
                                   format_func=lambda x: opcao_info[x])
            
            if st.button("🔍 Consultar", use_container_width=True):
                with st.spinner("Consultando registros literários..."):
                    resultado = inteligencia.pesquisar_livro(st.session_state.livro, selecao)
                    st.markdown(resultado)

# Rodapé centralizado
st.divider()
st.html('<p class="centered">Desenvolvido com ❤️ por Leonardo Salin</p>')