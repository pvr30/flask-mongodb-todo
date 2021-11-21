from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
import datetime
from werkzeug.utils import redirect

app = Flask(__name__)

# database configuration
app.config['MONGODB_SETTINGS'] = {
'db':'flaskproject',
'host':'localhost',
'port':27017
}
db = MongoEngine(app)


# model
class Task(db.Document):
    task = db.StringField(required=True)
    created_date = db.DateTimeField(default=datetime.datetime.now())
    completed = db.BooleanField(default=False)

    def __str__(self):
        return self.task


@app.route('/')
def home():
    tasks = Task.objects()
    return render_template('home.html', tasks=tasks)


@app.route('/addtask', methods=['GET', 'POST'])
def addtask():
    if request.method == 'POST':
        task = request.form.get('task')
        Task(task=task).save()
    return redirect('/')


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edititem(id: str):
    task = Task.objects(id=id).first()
    if request.method == 'POST':
        updated_task = request.form.get('task')
        task.update(task=updated_task)
        task.save()
        return redirect('/')
    return render_template('edit.html', task=task)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def deleteitem(id: str):
    task = Task.objects(id=id).first()
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render_template('delete.html', task=task)


@app.route('/complete/<id>', methods=['GET', 'POST'])
def complete(id: str):
    if request.method == 'POST':
        task = Task.objects(id=id).first()
        task.update(completed=True)
        task.save()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
