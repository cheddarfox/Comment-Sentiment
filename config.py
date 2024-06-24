DEBUG = True
MAX_COMMENTS = 1000  # Increased, but needs to be implemented in main script
SENTIMENT_THRESHOLD = 0.1
MAX_TOKENS = 4000  # Increased for more comprehensive analysis
TEMPERATURE = 0.7

# Add a new config for maximum content length if needed
MAX_CONTENT_LENGTH = 10000  # characters
AI_PROVIDER = 'openai'
# config.py
OPENAI_MODEL = "gpt-4o-2024-05-13"  # Your OpenAI model configuration remains unchanged
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"  # Updated Anthropoc model name
# Output path
OUTPUT_PATH = r"C:\Users\Scott\OneDrive\Documents\Fabric\CSAnalysis"
STANFORD_CORENLP_PATH = r'C:\Users\Scott\OneDrive\Coding\Comment Sentiment\stanford-corenlp-4.5.7'