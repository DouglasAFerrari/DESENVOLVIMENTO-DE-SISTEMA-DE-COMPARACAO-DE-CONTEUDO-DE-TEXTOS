from flask import Flask
import nltk
import os

# Função para baixar os dados necessários do NLTK
def download_nltk_data():
    """Verifica e baixa pacotes NLTK necessários se não existirem."""
    required_nltk_packages = {
        'corpora': ['stopwords', 'wordnet'], # wordnet pode ser útil para lematização futura
        'tokenizers': ['punkt'],
        'stemmers': ['rslp'] # Stemmer para Português
    }
    nltk_data_path = nltk.data.path[0] # Pega o primeiro caminho de dados do NLTK

    for category, packages in required_nltk_packages.items():
        for package in packages:
            try:
                # Tenta carregar o recurso para verificar se existe
                if category == 'corpora':
                    nltk.data.find(f'corpora/{package}')
                elif category == 'tokenizers':
                     nltk.data.find(f'tokenizers/{package}')
                elif category == 'stemmers':
                     nltk.data.find(f'stemmers/{package}')
                print(f"NLTK package '{package}' encontrado.")
            except LookupError:
                print(f"NLTK package '{package}' não encontrado. Baixando...")
                try:
                    nltk.download(package, quiet=True)
                    print(f"NLTK package '{package}' baixado com sucesso.")
                except Exception as e:
                    print(f"Erro ao baixar NLTK package '{package}': {e}")
                    print("Por favor, tente baixar manualmente executando:")
                    print(f"> python -m nltk.downloader {package}")
                    # Considerar sair ou lançar uma exceção mais séria se pacotes críticos faltarem

# Função factory para criar a instância da aplicação Flask
def create_app():
    """Cria e configura a instância da aplicação Flask."""
    app = Flask(__name__)

    # Configurações da aplicação (podem vir de variáveis de ambiente ou config file)
    # Ex: app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
    # Ex: app.config['UPLOAD_FOLDER'] = 'uploads' # Se for salvar arquivos temporariamente

    # Garante que os diretórios necessários existem (ex: upload folder)
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])

    # Baixa os dados do NLTK ao iniciar a aplicação
    print("Verificando dados do NLTK...")
    download_nltk_data()
    print("Verificação de dados do NLTK concluída.")


    # Registra as rotas (blueprints ou diretamente)
    with app.app_context():
        from . import routes

    print("Aplicação Flask criada e configurada.")
    return app