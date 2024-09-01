from flask import Flask, render_template, request, redirect, url_for, session
import os

#app = Flask(__name__)
def create_app():
    app = Flask(__name__)
    # configuration and routes here
    return app
app.secret_key = 'your_secret_key'

# Load questions from a text file
def load_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            question, *options, answer = line.strip().split(',')
            questions.append({
                'question': question,
                'options': options,
                'answer': answer
            })
    return questions

# Homepage with login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'user' and password == 'pass':  # Simple check
            session['username'] = username
            return redirect(url_for('select_quiz'))
    return render_template('login.html')

# Quiz selection page
@app.route('/select_quiz', methods=['GET', 'POST'])
def select_quiz():
    if request.method == 'POST':
        selected_quiz = request.form['quiz_file']
        session['quiz_file'] = selected_quiz
        return redirect(url_for('quiz'))
    quizzes = os.listdir('questions')
    return render_template('select_quiz.html', quizzes=quizzes)

# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    quiz_file = session.get('quiz_file')
    questions = load_questions(f'questions/{quiz_file}')
    if request.method == 'POST':
        score = 0
        for i, question in enumerate(questions):
            user_answer = request.form.get(f'question_{i}')
            if user_answer == question['answer']:
                score += 1
        session['score'] = score
        return redirect(url_for('result'))
    return render_template('quiz.html', questions=questions)

# Result page
@app.route('/result')
def result():
    username = session.get('username')
    score = session.get('score')
    return render_template('result.html', username=username, score=score)

if __name__ == '__main__':
    app.run(debug=True, port=5001)