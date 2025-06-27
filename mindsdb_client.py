import pandas as pd
import mindsdb_sdk
import json

server = mindsdb_sdk.connect('http://127.0.0.1:47334')

def query_knowledge_base(search_query: str, min_relevance: float = 0.25, metadata: dict = None):
    conditions = [f'content = "{search_query}"', f"relevance >= {min_relevance}"]

    if metadata:
        for key, value in metadata.items():
            conditions.append(f"{key} = '{value}'")

    condition_sql = " AND ".join(conditions)
    sql = f"SELECT * FROM my_bingekb WHERE {condition_sql};"

    print("Final SQL:", sql) 

    query = server.query(sql)
    df = query.fetch()

    if df.empty:
        return []

    results = []
    for _, row in df.iterrows():
        try:
            metadata_obj = json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata']
        except Exception:
            metadata_obj = {}

        results.append({
            "id": row['id'],
            "chunk_content": row['chunk_content'],
            "relevance": row['relevance'],
            "metadata": metadata_obj
        })

    return results



def query_agent(query: str):
    sql = f"""
SELECT answer
FROM my_agent 
WHERE question = "{query}";
    """
    query = server.query(sql)
    df = query.fetch()
    
    if df.empty:
        return []

    return df

