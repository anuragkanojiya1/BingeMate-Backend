-- 1. Create a Knowledge Base called "my_bingekb"
-- This stores embedded movie & series metadata using Ollama for both embeddings and reranking.

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

-- 2. Insert data into the knowledge base from a table named "BingeWatch"
-- The source is a previously uploaded file "files.BingeWatch"
-- It pulls both content and metadata fields into the knowledge base

INSERT INTO my_bingekb
SELECT Title, Type, Year, Genre, IMDb_Rating, Summary
FROM files.BingeWatch;

-- 3. Create an Agent called "my_agent"
-- This agent uses Gemini 2.0 Flash and references the "my_bingekb" knowledge base
-- It will answer questions based on the prompt and the KB content

CREATE AGENT my_agent
USING
    model = 'gemini-2.0-flash',
    google_api_key = 'your-google-studio-api-key',  -- Replace with actual key
    include_knowledge_bases= ['mindsdb.my_bingekb'],
    prompt_template='
        mindsdb.my_bingekb stores movies and series data
    ';
