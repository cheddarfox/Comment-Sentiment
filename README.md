# Comment Sentiment Analysis Project

This project performs sentiment analysis on comments using various NLP tools and AI models, including Stanford NLP, OpenAI, and Anthropic.

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

1. Download and install Java Development Kit (JDK) 11 or higher from [Oracle](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) or [OpenJDK](https://adoptopenjdk.net/).

2. Set up the JAVA_HOME environment variable:
   - Windows:
     1. Right-click on 'This PC' or 'My Computer' and select 'Properties'
     2. Click on 'Advanced system settings'
     3. Click on 'Environment Variables'
     4. Under 'System variables', click 'New'
     5. Set Variable name as JAVA_HOME
     6. Set Variable value as the path to your Java installation (e.g., C:\Program Files\Java\jdk-11)
   - macOS/Linux:
     Add the following to your ~/.bash_profile or ~/.zshrc:
     ```
     export JAVA_HOME=/path/to/your/java/home
     export PATH=$JAVA_HOME/bin:$PATH
     ```

3. Verify the installation by opening a new terminal and typing:
   ```
   java -version
   ```

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

You can modify the following settings in `config.py`:
- `MAX_CONTENT_LENGTH`: Maximum number of characters to analyze
- `AI_PROVIDER`: Choose between 'openai' and 'anthropic' for AI analysis
- `OPENAI_MODEL` and `ANTHROPIC_MODEL`: Specify the AI model to use
- `OUTPUT_PATH`: Directory for saving analysis results
- `STANFORD_CORENLP_PATH`: Path to Stanford CoreNLP installation

## Usage

The main script for this project is `comment_analyzer.py`. It can analyze text from various file formats and provide sentiment and engagement analysis along with AI-powered insights.

### Analyzing a File

To analyze a file, use the following command:

```
python comment_analyzer.py <path_to_file>
```

Supported file formats:
- Text files (.txt, .md)
- Microsoft Word documents (.docx)
- PDF files (.pdf)
- OpenDocument Text files (.odt)

Example:
```
python comment_analyzer.py sample_comment.txt
```

The script will output the analysis results to the console and save them in a Markdown file in the directory specified by `OUTPUT_PATH` in `config.py`.

### Output

The analysis output includes:

1. Sentiment Analysis:
   - Overall Sentiment Score
   - Interpretation (Very Negative, Negative, Neutral, Positive, Very Positive)
   - Stanford Sentiment Score
   - Sentence-level Sentiments

2. Engagement Analysis:
   - Overall Engagement Score (0-100)
   - Interpretation (Very Low, Low, Moderate, High, Very High Engagement)
   - Raw Engagement Score
   - Text Length
   - Counts of Likes, Dislikes, Replies, Questions, and Exclamations

3. AI Analysis:
   - Summary of overall sentiment and main topics
   - Detailed analysis including key discussion points and recommendations
   - Confidence score for the analysis

### Benchmarking Sentiment Analysis

To run the sentiment analysis benchmark, which tests the accuracy of the sentiment analysis against the Stanford Sentiment Treebank dataset, use the following command:

```
python comment_analyzer.py --benchmark
```

This will:
- Load the Stanford Sentiment Treebank dataset
- Analyze 100 sentences from the dataset
- Compare the predicted sentiments with the true sentiments
- Output the accuracy of the sentiment analysis

### Note on Stanford CoreNLP

The script automatically starts and stops the Stanford CoreNLP server as needed. Ensure that the `STANFORD_CORENLP_PATH` in `config.py` is correctly set to your Stanford CoreNLP installation directory.

### Interpreting Results

- Sentiment scores range from 0 (Very Negative) to 4 (Very Positive)
- Engagement scores range from 0 to 100, with higher scores indicating higher engagement
- The AI analysis provides a detailed interpretation of the text, including key points and recommendations

For any issues or unexpected results, check the log files for detailed error messages and debugging information.

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

