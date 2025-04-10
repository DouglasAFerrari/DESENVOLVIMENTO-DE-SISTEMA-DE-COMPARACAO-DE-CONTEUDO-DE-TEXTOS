from flask import current_app, request, jsonify, render_template
from .text_processing import extract_text, preprocess_text
from .similarity import calculate_similarity
import traceback # Para log de erros detalhado

# Importa a instância 'app' implicitamente via current_app ou define explicitamente
# from flask import Blueprint
# main_bp = Blueprint('main', __name__)
# @main_bp.route(...)
# Em __init__.py: app.register_blueprint(main_bp)

# Usando rotas diretamente na instância 'app' por simplicidade
@current_app.route('/')
def index():
    """Serve a página HTML principal."""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Erro ao renderizar index.html: {e}")
        # Retornar uma página de erro simples ou logar
        return "Erro ao carregar a página inicial.", 500


@current_app.route('/compare', methods=['POST'])
def compare_files():
    """Endpoint da API para comparar dois arquivos enviados."""
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Requisição inválida: Faltando um ou ambos os arquivos (file1, file2)."}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "Requisição inválida: Um ou ambos os arquivos não têm nome."}), 400

    print(f"Recebendo arquivos: '{file1.filename}' e '{file2.filename}'")

    text1_raw, text2_raw = None, None
    processed_text1, processed_text2 = None, None
    similarity_score = 0.0

    try:
        # 1. Extrair texto
        print("Iniciando extração de texto...")
        text1_raw = extract_text(file1.stream, file1.filename)
        text2_raw = extract_text(file2.stream, file2.filename)
        print("Extração de texto concluída.")

        if text1_raw is None or text2_raw is None:
             # A função extract_text já imprime logs específicos
             return jsonify({"error": "Não foi possível extrair texto de um ou ambos os arquivos. Verifique os logs do servidor e os formatos de arquivo."}), 400

        # 2. Pré-processar texto
        print("Iniciando pré-processamento...")
        processed_text1 = preprocess_text(text1_raw)
        processed_text2 = preprocess_text(text2_raw)
        print("Pré-processamento concluído.")

        if processed_text1 is None or processed_text2 is None:
            # A função preprocess_text já imprime logs
            return jsonify({"error": "Não foi possível processar o conteúdo textual após extração (pode ter resultado em texto vazio após limpeza)."}), 400

        # 3. Calcular similaridade
        print("Calculando similaridade...")
        similarity_score = calculate_similarity(processed_text1, processed_text2)
        print(f"Similaridade calculada: {similarity_score:.4f}")

        # 4. Retornar resultado
        return jsonify({
            "correlation_index": similarity_score,
            "filename1": file1.filename,
            "filename2": file2.filename
        })

    except LookupError as le:
        # Erro específico se pacote NLTK estiver faltando
        print(f"Erro de LookupError (pacote NLTK faltando?): {le}")
        traceback.print_exc() # Log completo do erro
        return jsonify({"error": f"Erro interno do servidor: Pacote NLTK necessário não encontrado ({le}). Verifique a instalação e os dados NLTK."}), 500
    except Exception as e:
        # Captura genérica para outros erros inesperados
        print(f"Erro inesperado no endpoint /compare: {e}")
        traceback.print_exc() # Log completo do erro
        return jsonify({"error": "Erro interno inesperado no servidor durante o processamento. Verifique os logs."}), 500