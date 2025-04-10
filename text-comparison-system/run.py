import os
from dotenv import load_dotenv
from app import create_app

# Carrega variáveis de ambiente do arquivo .env 
load_dotenv()

# Cria a instância da aplicação Flask usando a factory function
app = create_app()

if __name__ == '__main__':
    # Obtém a porta da variável de ambiente ou usa 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    # Roda a aplicação    
    app.run(host='0.0.0.0', port=port, debug=(os.environ.get('FLASK_ENV') == 'development'))