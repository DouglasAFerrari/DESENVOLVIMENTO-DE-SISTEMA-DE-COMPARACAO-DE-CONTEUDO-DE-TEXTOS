import PyPDF2
import docx # python-docx
import nltk
import string
import re

def extract_text(file_stream, filename):
    """
    Extrai texto de um stream de arquivo baseado na extensão do nome do arquivo.

    Args:
        file_stream: O objeto de stream do arquivo (como retornado por request.files).
        filename (str): O nome original do arquivo (para verificar a extensão).

    Returns:
        str: O texto extraído do arquivo.
        None: Se o formato não for suportado ou ocorrer um erro na extração.
    """
    text = None
    try:
        if filename.lower().endswith('.txt'):
            # Decodifica assumindo UTF-8
            text = file_stream.read().decode('utf-8')
        elif filename.lower().endswith('.pdf'):
            reader = PyPDF2.PdfReader(file_stream)
            text_parts = []
            for page in reader.pages:
                try:
                    text_parts.append(page.extract_text())
                except Exception as page_error:
                     print(f"Erro ao extrair texto da página do PDF '{filename}': {page_error}")
                     # Continua para a próxima página
            text = "\n".join(filter(None, text_parts)) # Junta partes não vazias
        elif filename.lower().endswith('.docx'):
            document = docx.Document(file_stream)
            text_parts = [paragraph.text for paragraph in document.paragraphs]
            text = "\n".join(text_parts)
        else:
            print(f"Formato de arquivo não suportado: {filename}")
            return None # Formato não suportado explicitamente

        if text is not None and not text.strip():
             print(f"Arquivo '{filename}' parece estar vazio ou não contém texto extraível.")
             return None # Retorna None se o texto extraído for vazio

    except UnicodeDecodeError:
        print(f"Erro de decodificação ao ler '{filename}'. Tentando com 'latin-1'.")
        try:
            # Volta ao início do stream e tenta outra codificação
            file_stream.seek(0)
            text = file_stream.read().decode('latin-1')
            if not text.strip(): return None
        except Exception as e:
             print(f"Erro ao ler '{filename}' mesmo com 'latin-1': {e}")
             return None
    except Exception as e:
        print(f"Erro ao processar o arquivo '{filename}': {e}")
        return None

    return text


def preprocess_text(text):
    """
    Aplica pré-processamento ao texto: minúsculas, tokenização, remoção de
    pontuação/números, remoção de stopwords e stemming (Português).

    Args:
        text (str): O texto bruto a ser processado.

    Returns:
        str: O texto pré-processado como uma única string.
        None: Se o texto de entrada for None ou vazio.
    """
    if not text:
        return None

    # 1. Converter para minúsculas
    text = text.lower()

    # 2. Tokenização (divide o texto em palavras/tokens)
    try:
        tokens = nltk.word_tokenize(text, language='portuguese')
    except LookupError:
        print("Erro: Pacote 'punkt' do NLTK não encontrado. Execute download_nltk_data() ou baixe manualmente.")
        # Em um cenário real, poderia lançar uma exceção ou retornar None
        raise # Re-lança a exceção para ser tratada na rota
    except Exception as e:
        print(f"Erro inesperado durante a tokenização: {e}")
        raise

    # 3. Remoção de Pontuação e Números (mantém apenas palavras alfabéticas)
    # Mantém tokens que são puramente alfabéticos
    tokens = [token for token in tokens if token.isalpha()]

    # 4. Remoção de Stop Words (palavras comuns como 'o', 'a', 'de')
    try:
        stop_words = set(nltk.corpus.stopwords.words('portuguese'))
        tokens = [token for token in tokens if token not in stop_words]
    except LookupError:
        print("Erro: Pacote 'stopwords' do NLTK não encontrado. Execute download_nltk_data() ou baixe manualmente.")
        raise
    except Exception as e:
        print(f"Erro inesperado durante remoção de stopwords: {e}")
        raise


    # 5. Stemming (redução da palavra ao seu radical - para Português)
    try:
        stemmer = nltk.stem.RSLPStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
    except LookupError:
        print("Erro: Pacote 'rslp' (stemmer português) do NLTK não encontrado. Execute download_nltk_data() ou baixe manualmente.")
        raise
    except Exception as e:
        print(f"Erro inesperado durante stemming: {e}")
        raise

    # 6. Rejuntar os tokens processados em uma única string
    processed_text = ' '.join(tokens)

    if not processed_text.strip():
        print("Texto ficou vazio após pré-processamento.")
        return None # Retorna None se não sobrar nada útil

    return processed_text