from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- إعداد المفتاح السري (مخفي عن المستخدم) ---
API_KEY = "AIzaSyA51PNU9NGYjzJc8PHeWDq-HHKo6Sn2hN0"
genai.configure(api_key=API_KEY)

# إعداد النموذج
model = genai.GenerativeModel('gemini-1.5-flash')

# مخزن مؤقت للمحادثات (في المواقع الكبيرة يفضل استخدام قاعدة بيانات)
chat_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.remote_addr  # تمييز المستخدم عبر عنوان الـ IP
    user_input = request.json.get("message")
    
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    
    try:
        # إرسال الرسالة مع الاحتفاظ بسياق المحادثة (الذاكرة)
        response = chat_sessions[user_id].send_message(user_input)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "عذراً، حدث خطأ فني. يرجى المحاولة لاحقاً."}), 500

if __name__ == '__main__':
    app.run(debug=True)
