
# 🧠 Medical SLM Pipeline with RAG & FAISS

A full end-to-end pipeline to preprocess 200,000 medical research abstracts, generate embeddings using Sentence Transformers, build a FAISS vector index, and prepare the foundation for Retrieval-Augmented Generation (RAG)-based medical query systems.

## 📌 Project Overview

This project implements a **Specialized Language Model (SLM)** pipeline that processes structured medical abstracts and builds a retrieval backend for downstream NLP tasks like semantic search or RAG-based question answering for medical students and researchers.

## 📂 Features

- ✅ Preprocessing of structured medical abstracts
- ✅ Sentence-transformer-based text embedding
- ✅ FAISS index creation for vector search
- ✅ Modularized Airflow DAG pipeline
- ✅ Docker-based orchestration
- 🚧 Future: RAG-based chatbot with query handling

---

## 🏗️ Architecture

```
Raw JSON (200k Abstracts)
        |
        v
[Extract & Preprocess]
        |
        v
[Sentence Embeddings]
        |
        v
[FAISS Index + Metadata]
        |
        v
🔍 (Query Engine or RAG Pipeline)
```

---

## ⚙️ Tech Stack

- **Python 3.12**
- **Apache Airflow 2.9.1**
- **Docker + Docker Compose**
- **FAISS**
- **Hugging Face Sentence Transformers**
- **NumPy, JSON**
- **Git + GitHub**

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/vashchirag02/Medslm.git
cd Medslm
```

### 2. Build and start Docker containers

```bash
docker-compose up --build
```

### 3. Access Airflow UI

- Navigate to: [http://localhost:8080](http://localhost:8080)
- Login:
  - **Username**: `admin`
  - **Password**: `admin`

### 4. Trigger the DAG

Open the `medical_slm_pipeline` DAG and click "Trigger DAG".

---

## 📁 Project Structure

```
├── dags/                     # Airflow DAGs
│   └── medical_slm_pipeline.py
├── data/                     # Mounted data folder
│   ├── med_abstracts.json
│   ├── processed_abstracts.json
│   ├── embeddings.npy
│   ├── metadata.json
│   └── faiss.index
├── Dockerfile                # Custom Airflow Dockerfile
├── docker-compose.yml        # Docker Compose config
└── README.md                 # Project overview
```

---

## 🔮 Future Enhancements

- [ ] Integrate a **FastAPI-based medical chatbot**
- [ ] Add **query pipeline with context re-ranking**
- [ ] Implement **Guardrails** for safety & bias checks
- [ ] Support **quantized models** for inference

---

## 🤝 Contributing

Pull requests and ideas are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

[MIT](LICENSE)

---

## 🙋‍♂️ Maintainer

- [@vashchirag02](https://github.com/vashchirag02)
