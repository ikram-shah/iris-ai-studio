from sqlalchemy import create_engine, text
from flask import jsonify

def get_table_list(request):
    username = request.args.get('username')
    password = request.args.get('password')
    hostname = request.args.get('hostname')
    port = request.args.get('port')
    namespace = request.args.get('namespace')

    if not all([username, password, hostname, port, namespace]):
        return jsonify({'error': 'All parameters are required: username, password, hostname, port, namespace'}), 400

    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
    engine = create_engine(CONNECTION_STRING)

    with engine.connect() as conn:
        with conn.begin():
            sql = """
                    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'SQLUser'
                    """
            result = conn.execute(text(sql))
            table_list = [row[0] for row in result.fetchall()]

    engine.dispose()
    return jsonify({"tables": table_list})