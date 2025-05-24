from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log

DATA_PATH = '/opt/airflow/data/med_abstracts.json'
PROCESSED_PATH = '/opt/airflow/data/processed_abstracts.json'
INDEX_PATH = '/opt/airflow/data/faiss.index'
EMBEDDINGS_PATH = '/opt/airflow/data/embeddings.npy'
METADATA_PATH = '/opt/airflow/data/metadata.json'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'medical_slm_pipeline',
    default_args=default_args,
    description='SLM pipeline on 200k medical abstracts with embedding and RAG',
    schedule_interval=None,
    catchup=False
)

def extract_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found.")
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    log.info(f"Loaded dataset with {len(data)} abstracts from {DATA_PATH}")

def preprocess_data():
    with open(DATA_PATH, 'r') as f:
        raw_data = json.load(f)

    processed = []
    for entry in raw_data:
        sections = [entry.get(sec, '') for sec in ['BACKGROUND', 'OBJECTIVE', 'METHODS', 'RESULTS', 'CONCLUSIONS']]
        full_text = ' '.join(filter(None, sections))
        processed.append({"pmid": entry.get("pmid", ""), "text": full_text})

    with open(PROCESSED_PATH, 'w') as f:
        json.dump(processed, f, indent=2)
    log.info(f"Saved {len(processed)} processed abstracts to {PROCESSED_PATH}")

def generate_embeddings():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    with open(PROCESSED_PATH, 'r') as f:
        processed = json.load(f)

    texts = [doc["text"] for doc in processed]
    embeddings = model.encode(texts, show_progress_bar=True)

    np.save(EMBEDDINGS_PATH, embeddings)
    with open(METADATA_PATH, 'w') as f:
        json.dump([doc["pmid"] for doc in processed], f, indent=2)
    log.info(f"Generated embeddings for {len(texts)} documents.")

def build_faiss_index():
    embeddings = np.load(EMBEDDINGS_PATH)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    log.info(f"Saved FAISS index to {INDEX_PATH}")

# DAG Tasks
t1 = PythonOperator(task_id='extract_data', python_callable=extract_data, dag=dag)
t2 = PythonOperator(task_id='preprocess_data', python_callable=preprocess_data, dag=dag)
t3 = PythonOperator(task_id='generate_embeddings', python_callable=generate_embeddings, dag=dag)
t4 = PythonOperator(task_id='build_faiss_index', python_callable=build_faiss_index, dag=dag)

t1 >> t2 >> t3 >> t4
