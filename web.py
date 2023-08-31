from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
from utils import transcribe, create_html, summarise, clean_subtitles, embed_subtitles

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        
        if uploaded_file:
            name = uploaded_file.filename.split(".")[0]
            filename = uploaded_file.filename
            os.makedirs(f"static/transcriptions/{name}", exist_ok=True)
            dir_path = os.path.join('static/transcriptions', name)
            filepath = os.path.join(dir_path, filename)

            uploaded_file.save(filepath)
            session['file_path'] = filepath
            session['filename'] = filename
            return redirect(url_for('results'))  # Redirect to the results page

    return render_template('index.html')

# This is just a placeholder. In reality, you'd have a way to process and get the summary.
def get_summary():
    # Simulating a delay
    path = session['file_path']
    if os.path.exists(path.replace(".mp4", " summary.txt")):
        return open(path.replace(".mp4", " summary.txt"), "r", encoding="utf-8").read()
    else:
        if os.path.exists(path.replace(".mp4", ".txt")):
            with open(path.replace(".mp4", ".txt"), "r", encoding="utf-8") as f:
                s = summarise(f.read())
        else:
            s = clean_subtitles(open(path.replace(".mp4", ".srt"), "r", encoding="utf-8").read())
            with open(path.replace(".mp4", ".txt"), "w", encoding="utf-8") as f:
                f.write(s)
            s = summarise(s)
        with open(path.replace(".mp4", " summary.txt"), "w", encoding="utf-8") as f:
            f.write(s)
            return s

def get_timestamped():
    audio_path = session['file_path']
    title = session['filename']
    if os.path.exists(audio_path.replace(".mp4", ".srt")):
        srt = open(audio_path.replace(".mp4", ".srt"), "r", encoding="utf-8").read()
    else:
        srt = transcribe(title, audio_path)
    # srt = open("static/transcriptions/Reality of Software Development/Reality of Software Development.srt").read()
    return create_html(srt)

def get_original():
    path = session['file_path']  
    with open(path.replace(".mp4", ".srt"), "r", encoding="utf-8") as f:
        subtitles = embed_subtitles(f.read())
    return subtitles
        

@app.route('/path_to_summary_endpoint', methods=['GET'])
def summary_endpoint():
    summary = get_summary()
    return jsonify({'ready': True, 'content': summary})

@app.route('/path_to_timestamped_endpoint', methods=['GET'])
def timestamped_endpoint():
    timestamped = get_timestamped()
    return jsonify({'ready': True, 'content': timestamped})

@app.route('/path_to_original_endpoint', methods=['GET'])
def original_endpoint():
    original = get_original()
    return jsonify({'ready': True, 'content': original})

@app.route('/results', methods=['GET'])
def results():
    transcription = session.get('transcription', 'No transcription available.')
    file_name = session.get('filename')
    file_path = session.get('file_path')
    return render_template('results.html', transcription=transcription, file_name=file_name, file_path=file_path)

app.run(debug=True)

# @app.route('/path_to_cleaned_endpoint', methods=['GET'])
# def cleaned_endpoint():
#     sleep(1)
#     cleaned = get_cleaned()
#     return jsonify({'ready': True, 'content': cleaned})


# def get_cleaned():
#     return "The cleaned content here..."


