# database.py
from sqlalchemy import create_engine, text

def connect_to_database(username, password, hostname, port, namespace):
    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
    engine = create_engine(CONNECTION_STRING)
    return engine

def query_database(username, password, hostname, port, namespace, query):
    engine = connect_to_database(username, password, hostname, port, namespace)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = [list(row) for row in result.fetchall()]
            conn.close()
        return {'success': True, 'data': data}
    except Exception as e:
        return {'success': False, 'error': str(e)}
