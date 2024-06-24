import os
import json
from dotenv import load_dotenv
import openai
from anthropic import Anthropic
import config
import logging
import re
import math
from stanfordcorenlp import StanfordCoreNLP

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Initialize AI clients
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Initialize Stanford CoreNLP
nlp = None

from config import STANFORD_CORENLP_PATH

def start_stanford_server():
    global nlp
    if nlp is None:
        try:
            nlp = StanfordCoreNLP(config.STANFORD_CORENLP_PATH)
            # Instead of version, let's check if the server is responsive
            test_response = nlp.annotate("Test sentence.", properties={
                'annotators': 'tokenize,ssplit',
                'outputFormat': 'json'
            })
            if test_response:
                logging.info("Stanford CoreNLP server started successfully and is responsive")
            else:
                logging.warning("Stanford CoreNLP server started but may not be responsive")
        except Exception as e:
            logging.error(f"Failed to start Stanford CoreNLP server: {str(e)}")
            raise

def stop_stanford_server():
    global nlp
    if nlp:
        try:
            nlp.close()
            nlp = None
            logging.info("Stanford CoreNLP server stopped")
        except Exception as e:
            logging.error(f"Error stopping Stanford CoreNLP server: {str(e)}")

def analyze_sentiment_stanford(text):
    global nlp
    if nlp is None:
        start_stanford_server()
    
    max_chunk_size = 10000  # Adjust as needed
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    all_sentiments = []
    
    try:
        for i, chunk in enumerate(chunks):
            sentiment = nlp.annotate(chunk, properties={
                'annotators': 'sentiment',
                'outputFormat': 'json',
                'timeout': 60000,
            })
            logging.debug(f"Raw Stanford NLP response for chunk {i+1} (first 500 characters): {sentiment[:500]}")
            
            if not sentiment:
                logging.error(f"Empty sentiment response from Stanford NLP for chunk {i+1}")
                continue
            
            try:
                sentiment_data = json.loads(sentiment)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error in Stanford NLP analysis for chunk {i+1}: {str(e)}")
                logging.debug(f"Failed JSON content for chunk {i+1}: {sentiment[:500]}...")
                continue
            
            for sentence in sentiment_data.get('sentences', []):
                sentiment_score = int(sentence.get('sentimentValue', 2))
                all_sentiments.append(sentiment_score)
        
        if not all_sentiments:
            logging.warning("No valid sentiments were extracted from any chunks")
            return {
                "score": 2,
                "stanford_sentiment": 2,
                "sentence_sentiments": []
            }
        
        avg_sentiment = sum(all_sentiments) / len(all_sentiments)
        
        return {
            "score": avg_sentiment,
            "stanford_sentiment": avg_sentiment,
            "sentence_sentiments": all_sentiments
        }
    
    except Exception as e:
        logging.error(f"Error in Stanford NLP analysis: {str(e)}", exc_info=True)
        return {
            "score": 2,
            "stanford_sentiment": 2,
            "sentence_sentiments": []
        }


def calculate_engagement_score(text):
    try:
        likes = len(re.findall(r'\blike[sd]?\b', text, re.IGNORECASE))
        dislikes = len(re.findall(r'\bdislike[sd]?\b', text, re.IGNORECASE))
        replies = len(re.findall(r'\brepl(y|ies)\b', text, re.IGNORECASE))
        questions = text.count('?')
        exclamations = text.count('!')
        
        text_length = len(text.split())
        normalization_factor = math.log(text_length + 1)
        
        raw_score = (likes * 1.5 + replies * 4 - dislikes * 2 + questions * 2 + exclamations) / normalization_factor
        normalized_score = min(math.log(raw_score + 1) * 20, 100)
        
        return {
            "score": normalized_score,
            "likes": likes,
            "dislikes": dislikes,
            "replies": replies,
            "questions": questions,
            "exclamations": exclamations,
            "raw_score": raw_score,
            "text_length": text_length
        }
    except Exception as e:
        logging.error(f"Error in calculate_engagement_score: {str(e)}", exc_info=True)
        return {
            "score": 0,
            "likes": 0,
            "dislikes": 0,
            "replies": 0,
            "questions": 0,
            "exclamations": 0,
            "raw_score": 0,
            "text_length": 0
        }

def analyze_with_openai(text):
    try:
        prompt = f"""Analyze the following text for sentiment and key discussion points:

{text}

Please provide your analysis in the following format:
1. A brief 2-3 sentence summary of the overall sentiment and main topics.
2. A detailed analysis including:
   - Overall sentiment
   - Key discussion points (as bullet points)
   - Specific recommendations or action items based on the analysis
   - Conclusion
3. Provide a confidence score (0-100) for your analysis and explain why you chose this score.

Ensure your analysis is objective and based on the content provided."""

        response = openai.ChatCompletion.create(
            model=config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error in OpenAI analysis: {str(e)}", exc_info=True)
        return "Error in OpenAI analysis"

def analyze_with_anthropic(text):
    try:
        message = anthropic_client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze the following text for sentiment and key discussion points:

{text}

Please provide your analysis in the following format:
1. A brief 2-3 sentence summary of the overall sentiment and main topics.
2. A detailed analysis including:
   - Overall sentiment
   - Key discussion points (as bullet points)
   - Specific recommendations or action items based on the analysis
   - Conclusion
3. Provide a confidence score (0-100) for your analysis and explain why you chose this score.

Ensure your analysis is objective and based on the content provided."""
                }
            ]
        )
        return message.content
    except Exception as e:
        logging.error(f"Error in Anthropic analysis: {str(e)}", exc_info=True)
        return "Error in Anthropic analysis"

def analyze_discussion(text):
    logging.debug("Starting analyze_discussion")
    if not text or len(text) > config.MAX_CONTENT_LENGTH:
        logging.warning(f"Invalid input text length: {len(text)}")
        raise ValueError(f"Input text must be between 1 and {config.MAX_CONTENT_LENGTH} characters.")

    try:
        logging.debug("Starting Stanford server")
        start_stanford_server()
        logging.debug("Performing sentiment analysis")
        sentiment_analysis = analyze_sentiment_stanford(text)
        logging.debug("Performing engagement analysis")
        engagement_analysis = calculate_engagement_score(text)
        
        logging.debug("Performing AI analysis")
        ai_analysis = None
        if config.AI_PROVIDER.lower() == "openai":
            ai_analysis = analyze_with_openai(text)
        elif config.AI_PROVIDER.lower() == "anthropic":
            ai_analysis = analyze_with_anthropic(text)
        else:
            logging.warning(f"Invalid AI provider specified in config: {config.AI_PROVIDER}")
            ai_analysis = "Invalid AI provider specified in config."
        
        logging.debug("Analysis completed")
        return {
            "sentiment_analysis": sentiment_analysis,
            "engagement_analysis": engagement_analysis,
            "ai_analysis": ai_analysis
        }
    except Exception as e:
        logging.exception(f"Error in analyze_discussion: {str(e)}")
        return {
            "error": f"Error in analyze_discussion: {str(e)}",
            "sentiment_analysis": None,
            "engagement_analysis": None,
            "ai_analysis": None
        }
    finally:
        logging.debug("Stopping Stanford server")
        stop_stanford_server()

if __name__ == "__main__":
    try:
        start_stanford_server()
        test_text = "I really like this product! It's amazing and works great. What do you think about it?"
        result = analyze_discussion(test_text)
        print(json.dumps(result, indent=2))
    finally:
        stop_stanford_server()