from flask import Flask, render_template, request, redirect, url_for # type: ignore
import random
import time

app = Flask(__name__)

# Sample texts for typing test
texts_easy = [
    "A computer is an electronic machine that runs on electricity and it understands only binary language.",
    "The programming language is a tool to talk with the computer.",
    "The minimum energy needed by an electron to come out from a metal surface is called the work function."
]

texts_medium = [
    "The existence of discrete energy levels in an atom was directly verified in 1914.",
    "We would first define the wavefront: when we drop a small stone on a calm pool of water.",
    "Einstein showed from his theory of special relativity that it is necessary to treat mass as another form of energy."
]

texts_hard = [
    "The atomic mass of O found from mass spectroscopy experiments is seen to be 15.99493u.",
    "Consider a thin p-type silicon (p-Si) semiconductor wafer.",
    "Initially, diffusion current is large and drift current is small."
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_test', methods=['POST'])
def start_test():
    difficulty = request.form['difficulty']
    if difficulty == 'easy':
        text_chosen = random.choice(texts_easy)
    elif difficulty == 'medium':
        text_chosen = random.choice(texts_medium)
    else:
        text_chosen = random.choice(texts_hard)
    
    return render_template('test.html', text=text_chosen)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    original_text = request.form['original_text']
    user_input = request.form['user_input']
    time_taken = float(request.form['time_taken'])
    
    # Calculate WPM and errors
    words = original_text.split()
    user_words = user_input.split()
    errors = sum(1 for i in range(min(len(words), len(user_words))) if words[i] != user_words[i])
    wpm = (len(user_words) / (time_taken / 60)) if time_taken > 0 else 0
    
    # Calculate score (you can adjust the scoring logic as needed)
    score = max(0, 100 - (errors * 10))  # Simple scoring: 100 - (10 * number of errors)
    
    return render_template('result.html', wpm=wpm, errors=errors, score=score)

@app.route('/show_results', methods=['POST'])
def show_results():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)