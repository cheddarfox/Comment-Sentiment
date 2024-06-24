import logging
from dataset_handler import load_stanford_sentiment_data
from ai_discussion_analyzer import analyze_sentiment_stanford

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def benchmark_sentiment_analysis(data_dir):
    data, phrase_sentiments = load_stanford_sentiment_data(data_dir)
    
    logging.info(f"Loaded {len(data)} sentences and {len(phrase_sentiments)} phrase sentiments")

    correct_predictions = 0
    total_predictions = 0

    for _, row in data.iterrows():
        sentence = row['sentence']
        sentence_id = row['sentence_id']
        
        logging.info(f"Processing sentence ID: {sentence_id}")
        logging.info(f"Sentence: {sentence}")

        matching_sentiment = phrase_sentiments[phrase_sentiments['phrase'] == sentence]
        
        if matching_sentiment.empty:
            logging.warning(f"No exact matching sentiment found for sentence ID: {sentence_id}")
            continue

        true_sentiment = matching_sentiment.iloc[0]['sentiment_class']
        
        analysis_result = analyze_sentiment_stanford(sentence)
        predicted_sentiment = interpret_sentiment(analysis_result['score'])
        
        logging.info(f"True sentiment: {true_sentiment}")
        logging.info(f"Predicted sentiment: {predicted_sentiment}")
        logging.info(f"Sentiment score: {analysis_result['score']:.4f}")
        logging.info(f"Stanford sentiment: {analysis_result['stanford_sentiment']:.4f}")
        logging.info("---")

        if predicted_sentiment == true_sentiment:
            correct_predictions += 1
        total_predictions += 1

        if total_predictions >= 100:  # Analyze 100 sentences
            break

    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    logging.info(f"Total predictions: {total_predictions}")
    logging.info(f"Correct predictions: {correct_predictions}")
    logging.info(f"Sentiment Analysis Accuracy: {accuracy:.2f}")

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

def compare_sentiments(true_sentiment, predicted_score):
    predicted_sentiment = interpret_sentiment(predicted_score)
    
    if true_sentiment == predicted_sentiment:
        return True
    elif abs(sentiment_to_score(true_sentiment) - predicted_score) <= 1:
        return True  # Consider it correct if it's off by at most one level
    else:
        return False

def sentiment_to_score(sentiment):
    sentiment_map = {
        "Very Negative": 0,
        "Negative": 1,
        "Neutral": 2,
        "Positive": 3,
        "Very Positive": 4
    }
    return sentiment_map.get(sentiment, 2)  # Default to Neutral if unknown

def benchmark_sentiment_analysis(data_dir):
    data, phrase_sentiments = load_stanford_sentiment_data(data_dir)
    
    logging.info(f"Loaded {len(data)} sentences and {len(phrase_sentiments)} phrase sentiments")

    correct_predictions = 0
    total_predictions = 0

    for _, row in data.iterrows():
        sentence = row['sentence']
        sentence_id = row['sentence_id']
        
        logging.info(f"Processing sentence ID: {sentence_id}")
        logging.info(f"Sentence: {sentence}")

        matching_sentiment = phrase_sentiments[phrase_sentiments['phrase'] == sentence]
        
        if matching_sentiment.empty:
            logging.warning(f"No exact matching sentiment found for sentence ID: {sentence_id}")
            continue

        true_sentiment = matching_sentiment.iloc[0]['sentiment_class']
        
        analysis_result = analyze_sentiment_stanford(sentence)
        predicted_score = analysis_result['score']
        predicted_sentiment = interpret_sentiment(predicted_score)
        
        is_correct = compare_sentiments(true_sentiment, predicted_score)
        
        logging.info(f"True sentiment: {true_sentiment}")
        logging.info(f"Predicted sentiment: {predicted_sentiment}")
        logging.info(f"Sentiment score: {predicted_score:.4f}")
        logging.info(f"Correct: {is_correct}")
        logging.info("---")

        if is_correct:
            correct_predictions += 1
        total_predictions += 1

        if total_predictions >= 100:  # Analyze 100 sentences
            break

    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    logging.info(f"Total predictions: {total_predictions}")
    logging.info(f"Correct predictions: {correct_predictions}")
    logging.info(f"Sentiment Analysis Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    data_dir = "Data/stanfordSentimentTreebank"
    benchmark_sentiment_analysis(data_dir)