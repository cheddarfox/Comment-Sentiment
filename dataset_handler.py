import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StanfordSentimentDataset:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.sentences = None
        self.phrases = None
        self.labels = None
        self.splits = None

    def load_data(self):
        try:
            sentences_path = os.path.join(self.data_dir, "datasetSentences.txt")
            phrases_path = os.path.join(self.data_dir, "dictionary.txt")
            labels_path = os.path.join(self.data_dir, "sentiment_labels.txt")
            splits_path = os.path.join(self.data_dir, "datasetSplit.txt")

            logging.info(f"Loading sentences from {sentences_path}")
            self.sentences = pd.read_csv(sentences_path, sep='\t', names=['sentence_id', 'sentence'])
            
            logging.info(f"Loading phrases from {phrases_path}")
            self.phrases = pd.read_csv(phrases_path, sep='|', names=['phrase', 'phrase_id'])
            
            logging.info(f"Loading labels from {labels_path}")
            self.labels = pd.read_csv(labels_path, sep='|', names=['phrase_id', 'sentiment_score'], skiprows=1)
            
            logging.info(f"Loading splits from {splits_path}")
            self.splits = pd.read_csv(splits_path, names=['sentence_id', 'split'])

            # Convert sentiment_score to float
            logging.info("Converting sentiment scores to float")
            self.labels['sentiment_score'] = pd.to_numeric(self.labels['sentiment_score'], errors='coerce')
            
            logging.info("Stanford Sentiment Dataset loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading Stanford Sentiment Dataset: {str(e)}")
            raise

    def get_processed_data(self):
        if self.sentences is None or self.phrases is None or self.labels is None or self.splits is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        data = self.sentences.merge(self.splits, on='sentence_id')
        
        # Merge phrases with labels
        phrase_sentiments = self.phrases.merge(self.labels, on='phrase_id')
        
        def score_to_class(score):
            if pd.isna(score):
                return "Unknown"
            elif score <= 0.2:
                return "Very Negative"
            elif score <= 0.4:
                return "Negative"
            elif score <= 0.6:
                return "Neutral"
            elif score <= 0.8:
                return "Positive"
            else:
                return "Very Positive"
        
        phrase_sentiments['sentiment_class'] = phrase_sentiments['sentiment_score'].apply(score_to_class)
        
        return data, phrase_sentiments

def load_stanford_sentiment_data(data_dir):
    dataset = StanfordSentimentDataset(data_dir)
    dataset.load_data()
    data, phrase_sentiments = dataset.get_processed_data()
    
    logging.info("Sample data:")
    logging.info(data.head())
    logging.info("\nSample phrase sentiments:")
    logging.info(phrase_sentiments.head())
    
    return data, phrase_sentiments