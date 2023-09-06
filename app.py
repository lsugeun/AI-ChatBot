from flask import Flask, render_template, request
from langdetect import detect
from translate import Translator
from textblob import TextBlob

app = Flask(__name__)
chat_history = []  # 대화 내용을 저장할 리스트

@app.route('/')
def home():
    return render_template('index.html', chat_history=chat_history, score=get_current_score())

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_input']

    # 언어 감지
    language = detect(user_message)

    # 번역 수행
    translator = Translator(to_lang="en", from_lang=language)
    translated_text = translator.translate(user_message)

    # 감정 분석 수행
    sentiment = TextBlob(translated_text).sentiment.polarity

    # 스코어 계산
    score = 0
    if sentiment > 0:
        bot_response = "긍정 문장입니다."
        score = 1
    elif sentiment < 0:
        bot_response = "부정 문장입니다."
        score = -1
    else:
        bot_response = "중립 문장입니다."

    # 이전 대화의 스코어 합산
    if chat_history:
        previous_score = chat_history[-1].get('score', 0)
        score += previous_score

    # 대화 내용 저장
    chat_history.append({
        "user_input": user_message,
        "translated_input": translated_text,
        "bot_response": bot_response,
        "score": score
    })

    return render_template('index.html', chat_history=chat_history, score=get_current_score())

def get_current_score():
    if chat_history:
        return chat_history[-1].get('score', 0)
    return 0

if __name__ == '__main__':
    app.run()
