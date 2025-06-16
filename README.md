# Research Paper Summarizer 📄✨

A Flask web application that uses BART (Bidirectional and Auto-Regressive Transformers) to automatically summarize research papers using state-of-the-art NLP techniques.

## Features

- **Smart Text Summarization**: Uses Facebook's BART-large-CNN model for high-quality abstractive summarization
- **User-Friendly Interface**: Clean, responsive web interface with real-time word counting
- **Text Processing**: Handles long documents by intelligently chunking and processing
- **Statistics**: Shows compression ratio, word counts, and processing metrics
- **Copy & Print**: Easy sharing and printing of results
- **API Endpoint**: RESTful API for programmatic access

## Quick Start

### 1. Setup Environment
```bash
# Create project directory
mkdir research-summarizer
cd research-summarizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Directory Structure
```
research-summarizer/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── style.css
```

### 4. Run the Application
```bash
python app.py
```

### 5. Open in Browser
Navigate to: `http://localhost:5000`

## How It Works

### Technical Architecture
1. **Input Processing**: Text is cleaned and preprocessed to remove noise
2. **Chunking**: Long documents are split into manageable chunks (900 words max)
3. **Summarization**: Each chunk is processed through BART-large-CNN model
4. **Post-processing**: Multiple summaries are combined and refined
5. **Output**: Final summary with statistics and metrics

### Model Details
- **Model**: `facebook/bart-large-cnn`
- **Type**: Encoder-Decoder Transformer
- **Training**: Fine-tuned on CNN/DailyMail dataset
- **Approach**: Abstractive summarization (generates new sentences)

## Usage Tips

### For Best Results:
- Include abstract, introduction, methodology, results, and conclusion
- Remove references, citations, and figure captions
- Ensure text is at least 50 words
- Use well-structured, academic text

### Supported Text Length:
- **Minimum**: 50 words
- **Maximum**: No hard limit (automatically chunked)
- **Optimal**: 500-2000 words

## API Usage

### POST `/api/summarize`
```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your research paper text here..."}'
```

### Response:
```json
{
  "summary": "Generated summary text...",
  "original_words": 1250,
  "summary_words": 185,
  "compression_ratio": 85.2
}
```

## Project Structure Explained

### `app.py`
- Main Flask application
- Handles routing and request processing
- Contains text processing and summarization logic
- Implements error handling and validation

### `templates/`
- **`index.html`**: Home page with input form
- **`result.html`**: Results page showing summary and statistics

### `static/style.css`
- Modern, responsive CSS styling
- Mobile-friendly design
- Print-optimized styles

## Troubleshooting

### Common Issues:

**1. Model Download Slow**
- First run downloads ~1.6GB model
- Subsequent runs are fast
- Ensure stable internet connection

**2. Memory Issues**
- Reduce `max_length` in summarizer calls
- Process shorter text chunks
- Close other applications

**3. Port Already in Use**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill existing process

**4. Import Errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Customization

### Adjust Summary Length:
```python
summary_result = summarizer(chunk, 
                          max_length=200,  # Longer summaries
                          min_length=80,   # Minimum length
                          do_sample=False)
```

### Use Different Models:
```python