import google.generativeai as genai

# Configuração única da API
def configurar_gemini(chave):
    genai.configure(api_key=chave)

# Inspeciona livro enviado (arquivo, foto, texto)
def inspecionar_livro(imagem):
    try:
        modelo = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = '''
        Analise a imagem e verifique se é uma capa de livro.
        
        Se NÃO for uma capa de livro, responda apenas:
        ERRO: Essa imagem não é uma capa de livro. Identificamos [descreva brevemente o que foi identificado].
        
        Se for uma capa de livro, identifique o título e forneça EXATAMENTE neste formato:
        Título: [título do livro]
        Autor: [nome do(s) autor(es)]
        Subtítulo: [subtítulo se houver]
        Editora: [nome da editora]
        Páginas: [número de páginas aproximadamente]
        Descrição: [breve descrição em 2-3 linhas]
        
        Importante: 
        - Use EXATAMENTE as palavras-chave acima (Título, Autor, etc)
        - Responda APENAS no formato solicitado, sem textos adicionais
        '''
        
        resposta = modelo.generate_content([prompt, imagem])
        texto = resposta.text.strip()
        
        if texto.startswith('ERRO:'):
            return {'erro': texto}
            
        livro = {}
        for linha in texto.split('\n'):
            if ':' in linha:
                chave, valor = linha.split(':', 1)
                livro[chave.strip()] = valor.strip()

        return livro
        
    except Exception as e:
        return {'erro': 'Ocorreu um erro ao processar a imagem. Por favor, tente novamente.'}

# Consulta informação específica do livro
def pesquisar_livro(livro, informacao):
    try:
        modelo = genai.GenerativeModel('gemini-2.0-flash')
        
        # Garantir que a pesquisa seja relacionada ao livro
        titulo = livro.get('Título', '')
        autor = livro.get('Autor', '')
        
        # Verificar se o livro existe
        consulta_existencia = f"""
        Verifique com MÁXIMA PRECISÃO se o livro "{titulo}" de {autor} existe de fato.
        
        IMPORTANTE:
        - NÃO faça suposições
        - NÃO tente adivinhar livros similares
        - NÃO considere livros de autores com nomes parecidos

        VERIFIQUE:
        - A correspondência EXATA entre título e autor
        - Se NÃO tiver certeza absoluta da existência do livro com ESSE título e ESSE autor específico, considere como não existente
        - Faça uma verificação cuidadosa baseada em seu conhecimento
        
        Responda APENAS:
        1. "EXISTE" - se você tem certeza que este livro existe, foi publicado e é real
        2. "NÃO_EXISTE" - se você tem certeza que este livro não existe ou não tem informações suficientes para confirmar
        
        Responda apenas com uma dessas palavras sem explicações adicionais.
        """
        
        verificacao = modelo.generate_content(consulta_existencia)
        resposta_verificacao = verificacao.text.strip().upper()
        
        # Se o livro não existir, informar ao usuário no mesmo formato que inspecionar_livro
        if resposta_verificacao == "NÃO_EXISTE":
            return {'erro': f'Não encontramos registros do livro "{titulo}", escrito por "{autor}".'}
        
        # Instrução geral para todas as consultas
        instrucao_geral = """
        INSTRUÇÕES DE FORMATO:
        - Inicie diretamente com o conteúdo solicitado
        - Não use introduções como "Com certeza", "Com prazer", "Aqui está", etc.
        - Não encerre com frases como "Espero que isso ajude", "Precisa de mais informações?", etc.
        - Mantenha o tom informativo e objetivo
        - Use formatação markdown para melhor organização
        """
        
        # Se o livro existe, proceder com a consulta principal
        prompts = {
            'Sobre': f'''{instrucao_geral}
                Forneça análise do livro "{titulo}" de {autor}:
                
                - Tema central e contexto da obra
                - Abordagem e metodologia utilizada
                - Principais argumentos e ideias
                - Contribuições para o campo/área
                - Público-alvo e relevância
                
                Limite: 150 linhas. Formatação em parágrafos objetivos.
                ''',
                
            'Resumo': f'''{instrucao_geral}
                Forneça resumo do livro "{titulo}" de {autor}:
                
                - Sintetize o conteúdo central
                - Destaque os argumentos principais
                - Comente as ideias e insights existentes
                - Apresente as conclusões essenciais e aprendizados
                
                Limite: 150 linhas. Mantenha estrutura clara e coesa da narrativa.
                ''',
                
            'Conceitos': f'''{instrucao_geral}
                Liste os 5 principais conceitos do livro "{titulo}" de {autor}:
                
                Para cada conceito:
                - Nome/título do conceito (negrito)
                - Breve explicação do conhecimento (3 linhas)
                
                Formato: conceito em negrito e breve descrição e contextualização em bullet point.
                ''',
                
            'Obras relacionadas': f'''{instrucao_geral}
                Recomende livros similares à "{titulo}" de {autor}:
                
                Liste 5 obras que:
                - Abordam temas semelhantes
                - Complementam o conhecimento
                - Importante que seja obra existente e publicada.
                
                Formato: título em negrito, autor entre aspas e breve descrição e justificativa de similaridade em bullet point
                ''',
                
            'Mais do autor': f'''{instrucao_geral}
                ##### Autor "{autor}":
                
                - Trajetória profissional e formação
                - Lista de obras mais relevantes e contribuições
                - Reconhecimento e impacto no campo
                
                Formato: texto organizado em tópicos com subtítulos.
                Verifique se as informações correspondem ao {autor} que escreveu "{titulo}". Não invente informações.
                ''',
                
            'Onde encontrar': f'''{instrucao_geral}
                Disponibilidade do livro "{titulo}" de {autor}:
                
                - Formatos disponíveis (físico, e-book, audiobook)
                - Principais livrarias e plataformas (separar por vírgula)
                - Bibliotecas e acervos relevantes
                - Informações adicionais de acesso
                
                Formato: sucinta e organizada por tipo de acesso.
                Verifique se as informações procedem e se o livro realmente está disponível.
                '''
        }
        
        resposta = modelo.generate_content(prompts[informacao])
        return resposta.text
        
    except Exception as e:
        return {'erro': 'Ocorreu um erro ao processar a consulta. Por favor, tente novamente.'}
