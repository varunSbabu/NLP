"""
===============================================
app.py

@Author : Varun AS, Syed Salahuddin quadri, Mohammad Omar

Components:
- Flask web server setup and configuration
- Text preprocessing and cleaning functions
- BART model initialization and summarization pipeline
- Route handlers for web interface (/summarize) and API (/api/summarize)
- Error handling and validation logic

Model Used: facebook/bart-large-cnn (1.6GB download on first run)
=================================================
"""




from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import re
import time

app = Flask(__name__)

# Initialize the summarization pipeline (this will download the model on first run)
print("Loading summarization model...")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("Model loaded successfully!")

def clean_text(text):
    """Clean and preprocess the input text"""
    # Remove extra whitespaces and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:-]', '', text)
    return text.strip()

def chunk_text(text, max_length=1000):
    """Split text into chunks for processing"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        # Get text from form
        input_text = request.form.get('text', '').strip()
        
        if not input_text:
            return render_template('result.html', 
                                 error="Please enter some text to summarize!")
        
        # Clean the text
        cleaned_text = clean_text(input_text)
        
        # Check if text is too short
        if len(cleaned_text.split()) < 50:
            return render_template('result.html',
                                 error="Text is too short. Please enter at least 50 words.")
        
        # Chunk text if it's too long
        chunks = chunk_text(cleaned_text, max_length=900)
        
        # Summarize each chunk
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            
            # Generate summary
            summary_result = summarizer(chunk, 
                                      max_length=150, 
                                      min_length=50, 
                                      do_sample=False)
            summaries.append(summary_result[0]['summary_text'])
        
        # Combine summaries if multiple chunks
        if len(summaries) > 1:
            combined_summary = ' '.join(summaries)
            # Summarize the combined summaries if too long
            if len(combined_summary.split()) > 200:
                final_summary = summarizer(combined_summary,
                                         max_length=200,
                                         min_length=80,
                                         do_sample=False)[0]['summary_text']
            else:
                final_summary = combined_summary
        else:
            final_summary = summaries[0]
        
        # Calculate stats
        original_words = len(input_text.split())
        summary_words = len(final_summary.split())
        compression_ratio = round((1 - summary_words/original_words) * 100, 1)
        
        return render_template('result.html',
                             original_text=input_text,
                             summary=final_summary,
                             original_words=original_words,
                             summary_words=summary_words,
                             compression_ratio=compression_ratio)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('result.html',
                             error=f"An error occurred: {str(e)}")

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Process similar to main route but return JSON
        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text, max_length=900)
        
        summaries = []
        for chunk in chunks:
            summary_result = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
            summaries.append(summary_result[0]['summary_text'])
        
        final_summary = ' '.join(summaries)
        
        return jsonify({
            'summary': final_summary,
            'original_words': len(text.split()),
            'summary_words': len(final_summary.split()),
            'compression_ratio': round((1 - len(final_summary.split())/len(text.split())) * 100, 1)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Research Paper Summarizer...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

