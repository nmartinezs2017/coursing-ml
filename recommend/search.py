
from sentence_transformers import util
from kedro.framework.context.context import load_context

context = load_context('../coursing-ml/')
df_ud = context.catalog.load("cleaned_udacity")
df_cou = context.catalog.load("cleaned_coursera")
corpus_embeddings_udacity = context.catalog.load("corpus_embeddings_udacity")
corpus_embeddings_coursera = context.catalog.load("corpus_embeddings_coursera")
model_udacity = context.catalog.load("nlp_model_udacity")
model_coursera = context.catalog.load("nlp_model_coursera")


def query_understanding(name_model, query):
    if (name_model == 'udacity'):
        embedding = model_udacity.encode(query, convert_to_tensor=True)
    elif (name_model == 'coursera'):
        embedding = model_coursera.encode(query, convert_to_tensor=True)
    return embedding


def top_k_retrieval(name_model, query_embedding, k = 10):
    if (name_model == 'udacity'):
        search_hits = util.semantic_search(query_embedding, corpus_embeddings_udacity, top_k=k)[0]
    elif (name_model == 'coursera'):
        search_hits = util.semantic_search(query_embedding, corpus_embeddings_coursera, top_k=k)[0]
    return search_hits


def result_ranking(top_k, lista_descartados, df):
    results = dict()
    for hit in top_k:
        related_course = df.iloc[hit['corpus_id']]
        id_hit = int(hit['corpus_id'])
        if id_hit not in lista_descartados:
            results[str(hit['corpus_id'])] = {"score": float(hit['score']), "title": related_course['title'], "url": related_course["url"] }
    return results


def search_courses_udacity(query, contexto, k=10):
    query_embedding = query_understanding("udacity", query)
    len_context = len(contexto)

    top_k = top_k_retrieval("udacity", query_embedding, k+len_context)

    results = result_ranking(top_k, contexto, df_ud)
    return results


def search_courses_coursera(query, contexto, k=10):
    query_embedding = query_understanding("coursera", query)
    len_context = len(contexto)

    top_k = top_k_retrieval("coursera", query_embedding, k+len_context)

    results = result_ranking(top_k, contexto, df_cou)
    return results