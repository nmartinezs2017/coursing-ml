from fastapi import FastAPI
from typing import Optional
from sentence_transformers import SentenceTransformer, util
from kedro.framework.context.context import load_context

app = FastAPI()

context = load_context('./')

model = SentenceTransformer('allenai-specter')
df = context.catalog.load("preprocessed_udacity")
corpus_embeddings = context.catalog.load("corpus_embeddings")

def search_courses(title, description = ""):
    query_embedding = model.encode(title+' '+description, convert_to_tensor=True)

    search_hits = util.semantic_search(query_embedding, corpus_embeddings)
    search_hits = search_hits[0]  #Get the hits for the first query

    results = dict()
    print("\n\nCourse:", title)
    print("Most similar course:")
    for hit in search_hits:
        related_paper = df.iloc[hit['corpus_id']]
        results[str(hit['corpus_id'])] = float(hit['score'])
        # print("{:.2f}\t{}".format(hit['score'], related_paper))

    return dict(results)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/semantic_search/{title}")
def read_item(title: str, description: Optional[str] = ""):
    list_courses = search_courses(title, description)
    return list_courses