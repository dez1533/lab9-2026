from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# Початковий список витрат для Варіанту 8 («Трекер витрат»)
tasks = [
    {"id": 1, "content": "Продукти в супермаркеті", "amount": 850.0, "category": "Їжа", "date": "2026-11-10", "done": True},
    {"id": 2, "content": "Оплата інтернету (GPON)", "amount": 400.0, "category": "Комунальні", "date": "2026-11-12", "done": True},
    {"id": 3, "content": "Дизельне пальне (АЗС)", "amount": 1600.0, "category": "Авто", "date": "2026-11-15", "done": False},
]
task_id_counter = 3


@app.route('/')
def index():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    filtered_tasks = tasks
    if start_date:
        filtered_tasks = [t for t in filtered_tasks if t.get('date', '') >= start_date]
    if end_date:
        filtered_tasks = [t for t in filtered_tasks if t.get('date', '') <= end_date]

    total_amount = sum(t.get('amount', 0.0) for t in filtered_tasks)

    return render_template(
        'index.html',
        tasks=filtered_tasks,
        total_amount=total_amount,
        start_date=start_date,
        end_date=end_date,
        today=date.today().isoformat()
    )


@app.route('/add', methods=['POST'])
def add():
    global task_id_counter
    task_content = request.form.get('content', '').strip()
    amount_raw = request.form.get('amount', '0').strip()
    category = request.form.get('category', 'Інше').strip() or 'Інше'
    exp_date = request.form.get('date') or date.today().isoformat()

    try:
        amount = float(amount_raw)
    except ValueError:
        amount = 0.0

    if task_content:
        task_id_counter += 1
        new_task = {
            'id': task_id_counter,
            'content': task_content,
            'amount': amount,
            'category': category,
            'date': exp_date,
            'done': False
        }
        tasks.append(new_task)
    return redirect(url_for('index'))


@app.route('/done/<int:id>')
def done(id):
    for task in tasks:
        if task['id'] == id:
            task['done'] = True
            break
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    global tasks
    tasks = [task for task in tasks if task['id'] != id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)