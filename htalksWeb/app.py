from flask import Flask, render_template, request, jsonify, url_for
from PIL import Image
import random
import os
from rapidfuzz import fuzz

app = Flask(__name__)

# Path to the folder containing images
IMAGE_FOLDER = 'static/images'

# Quiz questions and answers
questions = [
    {"image": "image1.png", "answer": {"ulan bu sürahi mi", "abi sürahiyle içseydin"}},
    {"image": "image2.png", "answer": {"çok zor ya"}},
    {"image": "image3.png", "answer": {"bertrand traore mi", "dango auttora mı"}},
    {"image": "image4.png", "answer": {"evertona sesleniş"}},
    {"image": "image5.png", "answer": {"cucurella"}},
    {"image": "image6.png", "answer": {"bi tane sol bek çocuk vardı", "beşiktaş feda sezonu"}},
    {"image": "image7.png", "answer": {"gider miyiz gidemedik", "zeki topçuya bayılırım", "aruno kone mi yaptı bu videoyu"}},
    {"image": "image8.png", "answer": {"ideal otobüs yolculuğu"}},
    {"image": "image9.png", "answer": {"benim kafanın içinden çık seni dava ederim", "başka bi şey düşünemiyorum"}},
    {"image": "image10.png", "answer": {"ya fivhs galatasaray maç bile oynamıyo"}},
    {"image": "image11.png", "answer": {"kaleciyi oynatıyo ananın amını oynat"}},
    {"image": "image12.png", "answer": {"ameliyat anısı"}},
    {"image": "image13.png", "answer": {"ulan be ordaydık", "hakemde takım elbise ceket var fener"}},
    {"image": "image14.png", "answer": {"devam gibi geldi", "olabilir abi futbolun içinde var bunlar", "şu kadar taklalık ne var ya"}},
    {"image": "image15.png", "answer": {"abi versatil ne demek", "versatil oyuncu", "okazyonlu topçu"}},
    {"image": "image16.png", "answer": {"ulan hulk sen de adam değilsin"}},
]

random.shuffle(questions)
current_question_index = 0
score = 0
SIMILARITY_THRESHOLD = 50  # Minimum similarity score to accept an answer

@app.route("/")
def home():
    """Render the home page with the first question."""
    global current_question_index
    current_question_index = 0  # Reset to the first question
    return render_template("index.html", 
                           question=questions[current_question_index], 
                           index=current_question_index, 
                           score=score)

@app.route("/submit", methods=["POST"])
def check_answer():
    """Process the user's answer and return the result."""
    global current_question_index, score
    user_answer = request.form.get("answer")
    current_index = int(request.form.get("index"))
    correct_answers = questions[current_index]["answer"]
    
    # Check answer similarity
    is_correct = False
    for correct_answer in correct_answers:
        similarity = fuzz.ratio(user_answer.lower(), correct_answer.lower())
        if similarity >= SIMILARITY_THRESHOLD:
            is_correct = True
            break

    if is_correct:
        score += 1
        result = {"result": "correct", "score": score}
    else:
        result = {"result": "incorrect", "score": score}

    # Move to the next question
    current_question_index += 1
    if current_question_index < len(questions):
        result["next_question"] = {
            "image": url_for('static', filename=f"images/{questions[current_question_index]['image']}"),
            "index": current_question_index,
        }
    else:
        result["next_question"] = None  # No more questions, quiz finished

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
