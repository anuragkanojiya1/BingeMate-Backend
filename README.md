This project is a FastAPI backend for [BingeMate](https://github.com/anuragkanojiya1/BingeMate) querying a **MindsDB Knowledge Base** powered by **Ollama LLMs** and embedding models. It integrates:

- 🌐 FastAPI backend
- 🧠 MindsDB KB, Jobs, Agent
- 🦙 Ollama (Mistral + Granite embedding)
- 🐳 Docker for environment management

---

## 📦 Requirements

Before getting started, make sure you have installed:

- [Docker Desktop](https://www.docker.com/get-started)
- [Ollama](https://ollama.com/download)
- Python 3.8+

---

## 📁 Project Structure

project-root/
│── mindsdb_client.py     # MindsDB functions
├── main.py               # FastAPI backend
├── requirements.txt      # Python dependencies
├── bingewatch.csv        # Data for BingeMate
└── README.md             # This file


## 🧪 Step-by-Step Setup

### 1️⃣ Clone this repo

```bash
git clone https://github.com/your-username/BingeMate-Backend.git
cd BingeMate-Backend
```

### 2️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run MindsDB in Docker
```bash
docker run --name mindsdb_container -e MINDSDB_APIS=http,mysql -p 47334:47334 -p 47335:47335 mindsdb/mindsdb
```

### 4️⃣ Start Ollama and download models

Ollama must be running in the background.

```bash
ollama run granite-embedding
ollama run mistral
```

## 🤖 Configure MindsDB

Once MindsDB and Ollama are running, execute the following commands to set up:

### 📚 Create a Knowledge Base

```bash
CREATE KNOWLEDGE_BASE my_bingekb
USING
    embedding_model = {
        "provider": "ollama",
        "model_name": "granite-embedding",
        "base_url": "http://host.docker.internal:11434"
    },
    reranking_model = {
        "provider": "ollama",
        "model_name": "mistral",
        "base_url": "http://host.docker.internal:11434"
    },
    metadata_columns = ['Year', 'Type', 'Genre', 'IMDb_Rating'],
    content_columns = ['Title', 'Summary', 'IMDb_Rating'],
    id_column = 'Title';
```

### 📥 Insert Data into Knowledge Base

At first, you have to upload the bingewatch.csv given in this repo to mindsdb gui editor files in datasources section with the name ```BingeWatch```. 
Then use this command to insert all data from csv file to Knowledge Base ```my_bingekb```

```bash
INSERT INTO my_bingekb
SELECT Title, Type, Year, Genre, IMDb_Rating, Summary
FROM files.BingeWatch;
```

### 🧠 Create an Agent with Gemini

```bash
CREATE AGENT my_agent
USING
    model = 'gemini-2.0-flash',
    google_api_key = 'your-api-key',
    include_knowledge_bases= ['mindsdb.my_bingekb'],
    prompt_template='
        mindsdb.my_bingekb stores movies and series data
    ';
```

### 🚀 Run the FastAPI Server

```bash
uvicorn main:app --reload
```

As backend has been configured, now you can use BingeMate app by following this link - [BingeMate](https://github.com/anuragkanojiya1/BingeMate)
