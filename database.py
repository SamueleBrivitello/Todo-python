import sqlite3
from typing import List, Dict, Optional


DATABASE = 'tasks.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def get_all_tasks() -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    
    tasks = []
    for row in rows:
        tasks.append({
            'id': row['id'],
            'text': row['text'],
            'completed': bool(row['completed']),
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        })
    
    return tasks


def create_task(text: str) -> Dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tasks (text, completed) VALUES (?, ?)',
        (text, False)
    )
    conn.commit()
    task_id = cursor.lastrowid
    
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    return {
        'id': row['id'],
        'text': row['text'],
        'completed': bool(row['completed']),
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }


def update_task(task_id: int, text: Optional[str] = None, completed: Optional[bool] = None) -> Optional[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task is None:
        conn.close()
        return None
    
    if text is not None and completed is not None:
        cursor.execute(
            'UPDATE tasks SET text = ?, completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (text, completed, task_id)
        )
    elif text is not None:
        cursor.execute(
            'UPDATE tasks SET text = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (text, task_id)
        )
    elif completed is not None:
        cursor.execute(
            'UPDATE tasks SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (completed, task_id)
        )
    
    conn.commit()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    return {
        'id': row['id'],
        'text': row['text'],
        'completed': bool(row['completed']),
        'created_at': row['created_at'],
        'updated_at': row['updated_at']
    }


def delete_task(task_id: int) -> Optional[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()
    
    if task is None:
        conn.close()
        return None
    
    deleted_task = {
        'id': task['id'],
        'text': task['text'],
        'completed': bool(task['completed']),
        'created_at': task['created_at'],
        'updated_at': task['updated_at']
    }
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return deleted_task
