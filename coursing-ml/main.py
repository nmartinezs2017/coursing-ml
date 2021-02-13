from fastapi import FastAPI
from typing import Optional
from sentence_transformers import SentenceTransformer, util
from kedro.framework.context.context import load_context

app = FastAPI()

context = load_context('./')

model = SentenceTransformer('allenai-specter')
df = context.catalog.load("preprocessed_udacity")
corpus_embeddings = context.catalog.load("corpus_embeddings")
df_cl = context.catalog.load("clustering_output_udacity")

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

@app.get("/semantic_search/")
def semantic_search(title: str, description: Optional[str] = ""):
    list_courses = search_courses(title, description)
    return list_courses

@app.get("/clustering/course-cluster/{id_course}")
def get_course_cluster(id_course: int):
    return {'id_course': id_course, 'clustering_id': df_cl.iloc[id_course]['Label']}

@app.get("/clustering/courses-list/{id_cluster}")
def get_list_cluster(id_cluster: int):
    list_courses = df_cl[df_cl['Label']==id_cluster].index.tolist()
    return {'clustering_id': id_cluster, 'list_courses': list_courses}

@app.get("/clustering/clusters-list/")
def get_list_cluster():
    list_courses = df_cl['Label'].unique().tolist()
    return {'list_courses': list_courses}