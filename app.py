from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import random
from collections import defaultdict

app = Flask(__name__)

# Dataset configuration
DATASETS = {
    'Botany': {
        '2024': 'Botny_Previous_Year 2024.csv',
        '2023': 'Botany_2023_Neet.csv',
        '2022': 'Botany_2022_Neet.csv',
        '2021': 'Botany_2021_Neet.csv',
        '2020': 'Botany_2020_Neet.csv',
        '2019': 'Botany_2019_Neet.csv',
        '2018': 'Botany_2018_Neet.csv',
        '2017': 'Botany_2017_Neet.csv',
        '2016': 'Botany_2016_Neet.csv',
    },
    'Zoology': {
        '2024': 'NEET2024_Zoology_previous_Questions.csv',
        '2023': 'Zoology_2023_NEET.csv',
        '2022': 'Zoology_2022_NEET.csv',
        '2021': 'Zoology_2021_NEET.csv',
        '2020': 'Zoology_2020_NEET.csv',
        '2019': 'Zoology_2019_NEET.csv',
        '2018': 'Zoology_2018_NEET.csv',
        '2017': 'Zoology_2017_NEET.csv',
        '2016': 'Zoology_2016_NEET.csv',
        
    },
    'Physics': {
        '2024': 'Physics2024PreviousYearQ&A.csv',
        '2023': 'Physics_Neet_2023.csv',
        '2022': 'Physics_2022_Neet_Unique_40_Questions.csv',
        '2021': 'Physics_2021_Neet_Unique_40_Questions.csv',
        '2020': 'Physics_2020_Neet_Unique_40_Questions.csv',
        '2019': 'Physics_2019_Neet_Unique_40_Questions.csv',
        '2018': 'Physics_2018_Neet_Unique_40_Questions.csv',
        '2017': 'Physics_2017_Neet_Unique_40_Questions.csv',
        '2016': 'Physics_2016_Neet_Unique_40_Questions.csv',
    },
    'Chemistry': {
        '2024': 'Chemistry_Previous_Year 2024.csv',
        '2023': 'Chemistry_2023_Neet_Unique_40_Questions.csv',
        '2021': 'Chemistry_2021_Neet_Unique_40_Questions (1).csv',
        '2020': 'Chemistry_2020_Neet_Unique_40_Questions (1).csv',
        '2019': 'Chemistry_2019_Neet_Unique_40_Questions.csv',
        '2017': 'Chemistry_2017_Neet_Unique_40_Questions.csv',
        '2016': 'Chemistry_2016_Neet_Unique_40_Questions.csv',
    }
}

DATA_DIR = 'data'

def load_questions(subject, year):
    filename = DATASETS[subject][year]
    filepath = os.path.join(DATA_DIR, subject, filename)
    df = pd.read_csv(filepath)
    questions = df.to_dict('records')
    return questions

def get_available_years(subject):
    return list(DATASETS[subject].keys())

def get_topics(subject, year):
    questions = load_questions(subject, year)
    topics = set()
    for q in questions:
        topics.add(q['Topic'])
    return sorted(topics)

@app.route('/')
def index():
    return render_template('index.html', subjects=DATASETS.keys())

@app.route('/subject/<subject>')
def subject(subject):
    years = get_available_years(subject)
    return render_template('subject.html', subject=subject, years=years)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        year = request.form['year']
        topic = request.form.get('topic', 'All')
        num_questions = int(request.form.get('num_questions', 10))
        
        questions = load_questions(subject, year)
        
        if topic != 'All':
            questions = [q for q in questions if q['Topic'] == topic]
        
        if len(questions) > num_questions:
            questions = random.sample(questions, num_questions)
        
        return render_template('quiz.html', 
                            questions=questions, 
                            subject=subject, 
                            year=year,
                            topic=topic)
    
    return redirect(url_for('index'))

@app.route('/results', methods=['POST'])
def results():
    user_answers = request.form.to_dict()
    questions = []
    correct = 0
    total = 0
    
    # Process the answers
    for key, value in user_answers.items():
        if key.startswith('q_'):
            q_id = int(key.split('_')[1])
            question = {
                'id': q_id,
                'question': user_answers[f'question_{q_id}'],
                'options': [
                    user_answers[f'optionA_{q_id}'],
                    user_answers[f'optionB_{q_id}'],
                    user_answers[f'optionC_{q_id}'],
                    user_answers[f'optionD_{q_id}']
                ],
                'correct_answer': user_answers[f'correct_{q_id}'],
                'user_answer': value,
                'subject': user_answers[f'subject_{q_id}'],
                'topic': user_answers[f'topic_{q_id}'],
                'year': user_answers[f'year_{q_id}']
            }
            questions.append(question)
            if value == question['correct_answer']:
                correct += 1
            total += 1
    
    score = (correct / total) * 100 if total > 0 else 0
    
    return render_template('results.html', 
                         questions=questions,
                         correct=correct,
                         total=total,
                         score=round(score, 2),
                         subject=questions[0]['subject'] if questions else '',
                         year=questions[0]['year'] if questions else '')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
