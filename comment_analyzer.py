import sys
import os
import textwrap
from datetime import datetime
import logging
from docx import Document as DocxDocument
from PyPDF2 import PdfReader
from odf.opendocument import load
from odf import text as odf_text
from ai_discussion_analyzer import analyze_discussion, start_stanford_server, stop_stanford_server
import config
from sentiment_benchmark import benchmark_sentiment_analysis

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    content = ""
    
    try:
        logging.debug(f"Attempting to read file: {file_path}")
        if file_extension.lower() in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        elif file_extension.lower() == '.docx':
            doc = DocxDocument(file_path)
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_extension.lower() == '.pdf':
            reader = PdfReader(file_path)
            content = '\n'.join([page.extract_text() for page in reader.pages if page.extract_text() is not None])
        elif file_extension.lower() == '.odt':
            doc = load(file_path)
            all_paragraphs = doc.getElementsByType(odf_text.P)
            content = '\n'.join([para.firstChild.data for para in all_paragraphs if para.firstChild is not None])
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        logging.debug(f"File read successfully. Content length: {len(content)}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        raise
    
    return content

def print_wrapped(text, width=100):
    for line in text.split('\n'):
        print('\n'.join(textwrap.wrap(line, width=width)))

def interpret_sentiment(score):
    if score <= 0.5:
        return "Very Negative"
    elif score <= 1.5:
        return "Negative"
    elif score <= 2.5:
        return "Neutral"
    elif score <= 3.5:
        return "Positive"
    else:
        return "Very Positive"

def interpret_engagement(score):
    if score >= 80:
        return "Very High Engagement"
    elif score >= 60:
        return "High Engagement"
    elif score >= 40:
        return "Moderate Engagement"
    elif score >= 20:
        return "Low Engagement"
    else:
        return "Very Low Engagement"

def save_analysis_result(analysis_result, file_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"analysis_result_{timestamp}.md"
    output_path = os.path.join(config.OUTPUT_PATH, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Analysis Result for {os.path.basename(file_path)}\n\n")
        f.write(f"Analysis performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Sentiment Analysis
        sa = analysis_result.get('sentiment_analysis', {})
        f.write("## Sentiment Analysis\n\n")
        f.write(f"- Overall Sentiment Score: {sa.get('score', 0):.2f}\n")
        f.write(f"- Interpretation: {interpret_sentiment(sa.get('score', 0))}\n")
        f.write(f"- Stanford Sentiment: {sa.get('stanford_sentiment', 'N/A'):.2f}\n")
        f.write(f"- Sentence Sentiments: {sa.get('sentence_sentiments', 'N/A')}\n\n")
        
        # Engagement Analysis
        ea = analysis_result.get('engagement_analysis', {})
        f.write("## Engagement Analysis\n\n")
        f.write(f"- Overall Engagement: {ea.get('score', 'N/A'):.1f}/100\n")
        f.write(f"- Interpretation: {interpret_engagement(ea.get('score', 0))}\n")
        f.write(f"- Raw Engagement Score: {ea.get('raw_score', 'N/A'):.2f}\n")
        f.write(f"- Text Length: {ea.get('text_length', 'N/A')} words\n")
        f.write(f"- Likes: {ea.get('likes', 'N/A')}\n")
        f.write(f"- Dislikes: {ea.get('dislikes', 'N/A')}\n")
        f.write(f"- Replies: {ea.get('replies', 'N/A')}\n")
        f.write(f"- Questions: {ea.get('questions', 'N/A')}\n")
        f.write(f"- Exclamations: {ea.get('exclamations', 'N/A')}\n\n")
        
        # AI Analysis
        f.write("## AI Analysis\n\n")
        f.write(analysis_result.get('ai_analysis', 'N/A'))
    
    print(f"Analysis result saved to: {output_path}")

def main(file_path):
    try:
        logging.debug("Starting analysis")
        start_stanford_server()
        logging.debug("Stanford server started")
        content = read_file(file_path)
        logging.debug(f"File read, content length: {len(content)}")
        if len(content) > config.MAX_CONTENT_LENGTH:
            content = content[:config.MAX_CONTENT_LENGTH]
            logging.debug(f"Content truncated to {config.MAX_CONTENT_LENGTH} characters")
        
        logging.debug(f"Analyzing file: {file_path}")
        logging.debug(f"Content (first 100 characters): {content[:100]}...")
        
        logging.debug("Performing analysis...")
        analysis_result = analyze_discussion(content)
        
        if 'error' in analysis_result:
            logging.error(f"Error in analysis: {analysis_result['error']}")
        else:
            logging.debug("Analysis completed successfully")
            # Print results to console
            print("\nSentiment Analysis:")
            sa = analysis_result['sentiment_analysis']
            print(f"Overall Sentiment Score: {sa['score']:.2f}")
            print(f"Interpretation: {interpret_sentiment(sa['score'])}")
            print(f"Stanford Sentiment: {sa['stanford_sentiment']:.2f}")
            print("Sentence Sentiments:")
            for i, sentiment in enumerate(sa['sentence_sentiments']):
                print(f"  Sentence {i+1}: {sentiment:.2f}")

            print("\nEngagement Analysis:")
            ea = analysis_result['engagement_analysis']
            print(f"Overall Engagement: {ea['score']:.1f}/100")
            print(f"Interpretation: {interpret_engagement(ea['score'])}")
            print(f"Raw Engagement Score: {ea['raw_score']:.2f}")
            print(f"Text Length: {ea['text_length']} words")
            print(f"Likes: {ea['likes']}")
            print(f"Dislikes: {ea['dislikes']}")
            print(f"Replies: {ea['replies']}")
            print(f"Questions: {ea['questions']}")
            print(f"Exclamations: {ea['exclamations']}")

            print("\nAI Analysis:")
            print_wrapped(analysis_result['ai_analysis'], width=100)

        # Save analysis result to file
        save_analysis_result(analysis_result, file_path)
    
    except Exception as e:
        logging.exception(f"Error processing file: {str(e)}")
    finally:
        stop_stanford_server()

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--benchmark":
        data_dir = "Data/stanfordSentimentTreebank"
        start_stanford_server()
        try:
            benchmark_sentiment_analysis(data_dir)
        finally:
            stop_stanford_server()
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"Usage: python {sys.argv[0]} <path_to_file> or --benchmark")