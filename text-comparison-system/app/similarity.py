from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(text1, text2):
    """
    Calcula a similaridade por cosseno entre dois textos usando TF-IDF.

    Args:
        text1 (str): O primeiro texto pré-processado.
        text2 (str): O segundo texto pré-processado.

    Returns:
        float: O índice de similaridade por cosseno (entre 0 e 1).
               Retorna 0.0 se um dos textos for None, vazio ou se ocorrer erro.
    """
    if not text1 or not text2:
        print("Um ou ambos os textos estão vazios após pré-processamento. Similaridade definida como 0.")
        return 0.0

    try:
        # Cria o corpus (lista de textos)
        corpus = [text1, text2]

        # Inicializa o vetorizador TF-IDF
        # Pode-se ajustar parâmetros como max_df, min_df, ngram_range aqui
        vectorizer = TfidfVectorizer()

        # Ajusta o vetorizador ao corpus e transforma os textos em vetores TF-IDF
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Calcula a matriz de similaridade por cosseno
        # O resultado é uma matriz 2x2:
        # [[sim(doc1,doc1), sim(doc1,doc2)],
        #  [sim(doc2,doc1), sim(doc2,doc2)]]
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)

        # Extrai a similaridade entre o documento 1 e o documento 2
        # Está em cosine_sim_matrix[0, 1] (ou [1, 0], é simétrico)
        similarity_score = cosine_sim_matrix[0, 1]

        # Garante que o score esteja no intervalo [0, 1] e não seja NaN
        if np.isnan(similarity_score):
            print("Score de similaridade resultou em NaN. Definindo como 0.")
            return 0.0

        return max(0.0, min(1.0, similarity_score)) # Garante intervalo [0, 1]

    except ValueError as ve:
        # Pode ocorrer se o vocabulário for vazio após pré-processamento (e.g., apenas stopwords)
        print(f"Erro de valor durante vetorização/similaridade (provavelmente vocabulário vazio): {ve}")
        return 0.0
    except Exception as e:
        print(f"Erro inesperado ao calcular similaridade: {e}")
        return 0.0