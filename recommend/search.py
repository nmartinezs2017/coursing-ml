from sentence_transformers import util
import pandas as pd

model_udacity = pd.read_pickle("models/nlp_model_udacity.pkl")
model_coursera = pd.read_pickle("models/nlp_model_coursera.pkl")
model_udemy = pd.read_pickle("models/nlp_model_udemy.pkl")

df_ud = pd.read_csv("datasets/cleaned_udacity.csv")
df_cou = pd.read_csv("datasets/cleaned_coursera.csv")
df_ude = pd.read_csv("datasets/cleaned_udemy.csv")

corpus_embeddings_udacity = pd.read_pickle("model_output/corpus_embeddings_udacity.pkl")
corpus_embeddings_coursera = pd.read_pickle("model_output/corpus_embeddings_coursera.pkl")
corpus_embeddings_udemy = pd.read_pickle("model_output/corpus_embeddings_udemy.pkl")


def query_to_embedding(name_model, query):
    if (name_model == 'udacity'):
        embedding = model_udacity.encode(query, convert_to_tensor=True)
    elif (name_model == 'coursera'):
        embedding = model_coursera.encode(query, convert_to_tensor=True)
    elif (name_model == 'udemy'):
        embedding = model_udemy.encode(query, convert_to_tensor=True)
    return embedding


def top_k_retrieval(name_model, query_embedding, k = 10):
    if (name_model == 'udacity'):
        search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=k)[0]
    elif (name_model == 'coursera'):
        search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=k)[0]
    elif (name_model == 'udemy'):
        search_hits = util.semantic_search(query_embedding, corpus_embeddings_udemy, top_k=k)[0]
    return search_hits


def result_ranking(top_k, lista_descartados, df):
    results = dict()
    for hit in top_k:
        related_course = df.iloc[hit['corpus_id']]
        id_hit = int(hit['corpus_id'])
        if id_hit not in lista_descartados:
            results[str(hit['corpus_id'])] = {"id": id_hit, "score": float(hit['score']), "title": related_course['title'], "url": related_course["url"] }
    return results


def search_courses_udacity(query, contexto, k=10):
    query_embedding = query_to_embedding("udacity", query)
    len_context = len(contexto)

    top_k = top_k_retrieval("udacity", query_embedding, k+len_context)

    results = result_ranking(top_k, contexto, df_ud)
    return results


def search_courses_coursera(query, contexto, k=10):
    query_embedding = query_to_embedding("coursera", query)
    len_context = len(contexto)

    top_k = top_k_retrieval("coursera", query_embedding, k+len_context)

    results = result_ranking(top_k, contexto, df_cou)
    return results


def search_courses_udemy(query, contexto, k=10):
    query_embedding = query_to_embedding("udemy", query)
    len_context = len(contexto)

    top_k = top_k_retrieval("udemy", query_embedding, k+len_context)

    results = result_ranking(top_k, contexto, df_ude)
    return results