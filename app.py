from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

mock_data = {
    "hello": "Hi there! How can I help you?",
    "bye": "Goodbye! Have a nice day.",
    "name?": "I'm your friendly chat bot.",
    "who is ibm ceo?": "aravind!"
    
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get-answer', methods=['POST'])
def get_answer():
    user_input = request.json.get('question').lower()  
    answer = mock_data.get(user_input, "Sorry, I don't understand that question.")  
    return jsonify({"answer": answer})  
if __name__ == '__main__':
    app.run(debug=True)