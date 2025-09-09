from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Inicializa o servidor Flask
app = Flask(__name__)
# Habilita o CORS para que a página HTML possa se comunicar com o servidor
CORS(app)

DATABASE = 'database.db'

# Conecta ao banco de dados e cria a tabela 'notes' se ela não existir
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

# Rota para adicionar uma nova nota
@app.route('/notes', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'A nota não pode estar vazia'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Nota adicionada com sucesso!'}), 201

# Rota para buscar todas as notas
@app.route('/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
    conn.close()
    
    # Converte os resultados do banco de dados para um formato JSON
    notes_list = [dict(note) for note in notes]
    return jsonify(notes_list)

if __name__ == '__main__':
    create_table()
    # Roda o servidor na porta 5000
    app.run(debug=True, port=5000)