from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
# Mock data as previously defined
data = {
    'thanosbuild': ['1.0.0.build-299', '1.0.0.build-201', '1.0.0.build-201'],
    'mzone': ['mzonep81', 'mzonep51', 'mzonep61'],
    'Location': ['lon1-qz1', 'wdc1-qz1', 'wdc2-qz1'],
    'region': ['lon04', 'wdc04', 'wdc06']
}
mock_data = {
    "What is the oldest thanosbuild in production?": "Hi there! How can I help you?",
    "What is the latest thanosbuild in production?": "Goodbye! Have a nice day.",
    "List all thanosbuild in production?": "I'm your friendly chat bot.",
    "What is the thanospodman value for wdc06 region": "aravind!",
    "What is the thanospodman value for wdc07 region?": "result known",
    "What thanosregistry column is in wdc07 region?": "answer found",
    "What thanosregistry value is in lon05 region?": "hanuma",
    "Which Location column is in region of par05?": "yes"
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get-answer', methods=['POST'])
def get_answer():
    user_input = request.json.get('question').strip()  # Keep original casing for better matching
    # Use a case-insensitive approach for matching
    answer = next((v for k, v in mock_data.items() if k.lower() == user_input.lower()), "Sorry, I don't understand that question.")
    return jsonify({"answer": answer})
@app.route('/get-autocomplete', methods=['POST'])
def get_autocomplete():
    query = request.json.get('query').lower().strip()
    suggestions = []
    # 1. Check if the query matches any header names.
    for header in data.keys():
        if query in header.lower() and header.lower() not in suggestions:
            suggestions.append(header.lower())  # Add the header to suggestions.
    # 2. If a header is typed out, suggest values under that header.
    if query in data.keys():
        for value in data[query]:
            if value.lower() not in suggestions:
                suggestions.append(value)
    # 3. Check for partial matches in the question list after full words.
    if len(query) > 3 or ' ' in query:
        for question in mock_data.keys():
            if query in question.lower() and question.lower() not in suggestions:
                suggestions.append(question)
    # 4. Data-based suggestions (Check data values in each column for matches).
    for header, values in data.items():
        for value in values:
            if query in value.lower() and value.lower() not in suggestions:
                suggestions.append(value.lower())
    return jsonify({"suggestions": suggestions})
if __name__ == '__main__':
    app.run(debug=True)