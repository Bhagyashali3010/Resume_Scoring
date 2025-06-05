from flask import Flask, render_template, request
import os
from resume_parse import extract_text_from_pdf, parse_resume_with_gemini
from scorer import score_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file uploaded"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Extract and parse resume
    text = extract_text_from_pdf(filepath)
    parsed_json_text = parse_resume_with_llama(text)
    total_score, breakdown = score_resume(parsed_json_text)

    return render_template('result.html', score=total_score, breakdown=breakdown, parsed=parsed_json_text)

if __name__ == '__main__':
    app.run(debug=True)
