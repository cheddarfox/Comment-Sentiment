# Comment Sentiment Analysis Project

This project performs sentiment analysis on comments using various NLP tools and AI models, including Stanford NLP.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Java Setup](#java-setup)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Dependencies](#dependencies)

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.8 or higher
- Conda (recommended) or virtualenv
- Java Development Kit (JDK) 11 or higher
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/cheddarfox/Comment-Sentiment.git
   cd Comment-Sentiment
   ```

2. Run the setup script:
   
   For Conda environment (recommended):
   ```
   python setup.py --conda
   ```

   For standard virtual environment:
   ```
   python setup.py
   ```

   This script will:
   - Create and activate the appropriate environment
   - Install required dependencies
   - Download Stanford CoreNLP models
   - Set up necessary directories
   - Create a template .env file for API keys

3. Activate the environment:
   
   For Conda:
   ```
   conda activate comment_sentiment
   ```

   For virtual environment:
   ```
   source venv/bin/activate  # On Unix or MacOS
   venv\Scripts\activate.bat  # On Windows
   ```

4. Configure your .env file with the necessary API keys.

## Java Setup

(Java setup instructions remain the same as in the previous version)

## Project Structure

The project structure should look like this after setup:

```
Comment-Sentiment/
│
├── .vscode/
│   ├── java-formatter.xml
│   └── settings.json
├── Data/
│   ├── MACOSX/
│   ├── stanfordSentimentTreebank/
│   ├── stanfordSentimentTreebankRaw/
│   └── stanford-corenlp-4.5.7/
├── .env
├── .gitignore
├── ai_discussion_analyzer.py
├── comment_analyzer.py
├── config.py
├── dataset_handler.py
├── environment.yml
├── README.md
├── requirements.txt
├── sentiment_benchmark.py
├── setup.py
└── StanfordNLPCore_Models_dL_install.py
```

## Configuration

The `.env` file contains configuration for API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Replace the placeholder values with your actual API keys.

## Usage

(Add instructions on how to run the main script and any other relevant usage information)

## Dependencies

The project relies on several Python packages and external tools. Key dependencies include:

- anthropic
- openai
- pandas
- scikit-learn
- stanfordnlp
- nltk
- textblob

For a full list of dependencies, refer to the `requirements.txt` and `environment.yml` files.

