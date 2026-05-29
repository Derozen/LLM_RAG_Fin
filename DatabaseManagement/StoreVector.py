import psycopg2


def store_vector(Chunks, embeddings,dbname,user,host,password):
    """
    Connect to the PostGreSQL database and create a table named documents with 3 columns: id, content and embedding.
    Chunks: A list of text chunks that we want to store in the database.
    emeddings: A list of vector embeddings corresponding tothe text chunks. Each embeding should  be a list of 384 float values. The embedding column in the database should be of type vector (384).
    """
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password
    )

    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)
    );
    """)

    conn.commit()
    data = list(zip(Chunks, embeddings))

    cur.executemany(
        """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s)
        """,
        data
    )

    conn.commit()

    cur.execute("""
    CREATE INDEX ON documents
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
    """)

    conn.commit()

    cur.execute("ANALYZE documents;")
    conn.commit()
    conn.close()

    print("Data stored successfully in the database.")