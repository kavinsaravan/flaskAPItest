from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# In-memory storage for demo purposes
todos = []


@app.route('/')
def index():
    """Display all todos organized by category"""
    # Group todos by category
    categories = {}
    for todo in todos:
        category = todo['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(todo)

    return render_template('index.html', categories=categories, enumerate=enumerate)


@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo item"""
    task = request.form.get('task')
    category = request.form.get('category')
    if task and category:
        todo = {
            'id': len(todos),
            'task': task,
            'category': category,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        todos.append(todo)
        flash('Task added successfully!', 'success')
    else:
        flash('Please enter both task and category!', 'error')

    return redirect(url_for('index'))


@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """Mark a todo as complete"""
    if 0 <= todo_id < len(todos):
        todos[todo_id]['completed'] = not todos[todo_id]['completed']
        status = 'completed' if todos[todo_id]['completed'] else 'reopened'
        flash(f'Task {status}!', 'success')
    else:
        flash('Task not found!', 'error')

    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo item"""
    if 0 <= todo_id < len(todos):
        deleted_task = todos.pop(todo_id)
        # Update IDs for remaining tasks
        for i, todo in enumerate(todos):
            todo['id'] = i
        flash('Task deleted!', 'success')
    else:
        flash('Task not found!', 'error')

    return redirect(url_for('index'))


@app.route('/api/todos')
def api_todos():
    """API endpoint to get all todos as JSON"""
    return {'todos': todos}


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


def create_templates():
    """Create HTML template files"""

    # Base template
    base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask Todo App{% endblock %}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
            border-radius: 10px;
            text-align: center;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .nav {
            margin-top: 1rem;
        }

        .nav a {
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .nav a:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }

        .flash-messages {
            margin-bottom: 1rem;
        }

        .flash {
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 5px;
            font-weight: 500;
        }

        .flash.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .flash.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .card {
            background: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e1e5e9;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        select {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e1e5e9;
            border-radius: 5px;
            font-size: 1rem;
            background-color: white;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 5px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }

        .btn-danger:hover {
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        }

        .btn-success {
            background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        }

        .btn-success:hover {
            box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
        }

        .todo-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem;
            margin-bottom: 0.5rem;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }

        .todo-item.completed {
            opacity: 0.7;
            border-left-color: #28a745;
        }

        .todo-item.completed .task-text {
            text-decoration: line-through;
        }

        .task-info {
            flex-grow: 1;
        }

        .task-text {
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
        }

        .task-meta {
            font-size: 0.8rem;
            color: #6c757d;
        }

        .task-actions {
            display: flex;
            gap: 0.5rem;
        }

        .btn-sm {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }

        .empty-state {
            text-align: center;
            padding: 3rem;
            color: #6c757d;
        }

        .empty-state h3 {
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }

        footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e1e5e9;
            color: #6c757d;
        }

        .category-section {
            margin-bottom: 2rem;
        }

        .category-header {
            color: #667eea;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e1e5e9;
        }

        .category-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 500;
            margin-right: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{% block header %}Flask Todo App{% endblock %}</h1>
            <nav class="nav">
                <a href="{{ url_for('index') }}">Home</a>
                <a href="{{ url_for('about') }}">About</a>
                <a href="{{ url_for('api_todos') }}">API</a>
            </nav>
        </header>

        <main>
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="flash-messages">
                        {% for category, message in messages %}
                            <div class="flash {{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}

            {% block content %}{% endblock %}
        </main>

        <footer>
            <p>Built with Flask &hearts;</p>
        </footer>
    </div>
</body>
</html>'''

    # Index template
    index_template = '''{% extends "base.html" %}

{% block content %}
<div class="card">
    <h2>Add New Task</h2>
    <form method="POST" action="{{ url_for('add_todo') }}">
        <div class="form-group">
            <label for="task">Task Description:</label>
            <input type="text" id="task" name="task" placeholder="Enter your task..." required>
        </div>
        <div class="form-group">
            <label for="category">Category:</label>
            <select id="category" name="category" required>
                <option value="">Select a category...</option>
                <option value="Work">Work</option>
                <option value="Other">Other</option>
            </select>
        </div>
        <button type="submit" class="btn">Add Task</button>
    </form>
</div>

<div class="card">
    <h2>Your Tasks</h2>

    {% if categories %}
        {% for category, category_todos in categories.items() %}
            <div class="category-section">
                <h3 class="category-header">{{ category }} ({{ category_todos|length }})</h3>
                {% for todo in category_todos %}
                    <div class="todo-item {% if todo.completed %}completed{% endif %}">
                        <div class="task-info">
                            <div class="task-text">{{ todo.task }}</div>
                            <div class="task-meta">
                                <span class="category-badge">{{ todo.category }}</span>
                                Created: {{ todo.created_at }}
                            </div>
                        </div>
                        <div class="task-actions">
                            <a href="{{ url_for('complete_todo', todo_id=todo.id) }}" 
                               class="btn btn-sm {% if todo.completed %}btn-success{% else %}btn-success{% endif %}">
                                {% if todo.completed %}Undo{% else %}Complete{% endif %}
                            </a>
                            <a href="{{ url_for('delete_todo', todo_id=todo.id) }}" 
                               class="btn btn-sm btn-danger"
                               onclick="return confirm('Are you sure you want to delete this task?')">
                                Delete
                            </a>
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% endfor %}
    {% else %}
        <div class="empty-state">
            <h3>No tasks yet!</h3>
            <p>Add your first task above to get started.</p>
        </div>
    {% endif %}
</div>
{% endblock %}'''

    # About template
    about_template = '''{% extends "base.html" %}

{% block title %}About - Flask Todo App{% endblock %}
{% block header %}About This App{% endblock %}

{% block content %}
<div class="card">
    <h2>About Flask Todo App</h2>
    <p>This is a simple todo application built with Flask, demonstrating:</p>
    <ul style="margin: 1rem 0; padding-left: 2rem;">
        <li>Flask routing and view functions</li>
        <li>HTML template rendering with Jinja2</li>
        <li>Form handling (POST requests)</li>
        <li>URL parameters and dynamic routes</li>
        <li>Flash messaging for user feedback</li>
        <li>JSON API endpoints</li>
        <li>Responsive CSS styling</li>
    </ul>

    <h3>Features</h3>
    <ul style="margin: 1rem 0; padding-left: 2rem;">
        <li>Add new tasks</li>
        <li>Mark tasks as complete/incomplete</li>
        <li>Delete tasks</li>
        <li>View task creation timestamps</li>
        <li>JSON API for programmatic access</li>
    </ul>

    <h3>API Usage</h3>
    <p>You can access the todos programmatically:</p>
    <code style="background: #f8f9fa; padding: 0.5rem; border-radius: 3px; display: block; margin: 1rem 0;">
        GET /api/todos - Returns all todos as JSON
    </code>

    <a href="{{ url_for('index') }}" class="btn">Back to Tasks</a>
</div>
{% endblock %}'''

    # Write template files
    with open('templates/base.html', 'w') as f:
        f.write(base_template)

    with open('templates/index.html', 'w') as f:
        f.write(index_template)

    with open('templates/about.html', 'w') as f:
        f.write(about_template)


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    # Create the HTML templates
    create_templates()

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5002)