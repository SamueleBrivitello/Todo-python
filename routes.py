from flask import render_template, request, jsonify
from database import get_all_tasks, create_task, update_task, delete_task


def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/tasks', methods=['GET'])
    def get_tasks():
        tasks = get_all_tasks()
        return jsonify(tasks)

    @app.route('/api/tasks', methods=['POST'])
    def add_task():
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Il testo della task è obbligatorio'}), 400
        
        new_task = create_task(data['text'])
        return jsonify(new_task), 201

    @app.route('/api/tasks/<int:task_id>', methods=['PUT'])
    def update_task_route(task_id):
        data = request.get_json()
        text = data.get('text')
        completed = data.get('completed')
        updated = update_task(task_id, text=text, completed=completed)
        
        if updated is None:
            return jsonify({'error': 'Task non trovata'}), 404
        
        return jsonify(updated)

    @app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task_route(task_id):
        deleted = delete_task(task_id)
        
        if deleted is None:
            return jsonify({'error': 'Task non trovata'}), 404
        
        return jsonify({
            'message': 'Task eliminata con successo',
            'task': deleted
        })
