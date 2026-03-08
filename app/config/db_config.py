import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="ep-rough-violet-ai56m94u-pooler.c-4.us-east-1.aws.neon.tech",
        port=5432,
        database="neondb",
        user="neondb_owner",
        password="npg_TVQhSkv53KFz",
    )