import os
from openai import OpenAI
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

client = OpenAI()
MODEL_PATH = "./model/Chinese-Emotion-model"

def get_sentiment(text):
    if not text: return "無資料"
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
        result = classifier(text)
        return f"{result[0]['label']} (信心度: {result[0]['score']:.2f})"
    except Exception as e:
        return f"分析失敗: {str(e)}"

def get_ai_advice(health_data):
    prompt = f"提供孕期建議：週數{health_data['week']}, 體重{health_data['weight']}, 症狀{health_data['symptoms']}"
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "AI 建議生成失敗"

def get_risk_prediction(health_data):
    prompt = f"評估風險：週數{health_data['week']}, 心律{health_data['heart_rate']}, 症狀{health_data['symptoms']}"
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "風險評估失敗"
