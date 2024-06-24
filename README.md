# Comment Sentiment Analysis Project

This project performs sentiment analysis on comments using various NLP tools and AI models.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Conda Environment Setup](#conda-environment-setup)
   - [Virtual Environment Setup](#virtual-environment-setup)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Dependencies](#dependencies)

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Python 3.8 or higher
- Java Development Kit (JDK)
- Visual Studio Code (or your preferred IDE)
- Conda (recommended) or virtualenv

## Installation

You can set up this project using either Conda (recommended) or a standard Python virtual environment.

### Conda Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create a new Conda environment:
   ```
   conda create -n comment_sentiment python=3.8
   conda activate comment_sentiment
   ```

3. Run the setup script:
   ```
   python setup.py --conda
   ```

### Virtual Environment Setup

If you prefer not to use Conda, you can set up a standard Python virtual environment:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Run the setup script:
   ```
   python setup.py
   ```

After running the setup script, regardless of the method:

3. Set up your environment variables:
   - Copy the `.env.example` file to `.env`
   - Fill in your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ANTHROPIC_API_KEY=your_anthropic_api_key_here
     ```

## Project Structure

The project structure should look like this after setup:

```
project_root/
│
├── .env
├── .gitignore
├── config.py
├── requirements.txt
├── StanfordNLPCore_Models_dL_install.py
├── main.py (to be created)
├── README.md
│
├── stanford-corenlp-4.5.7/
│
└── venv/ or conda_env/
```

(The rest of the README remains the same as before)

