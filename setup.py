import os
import subprocess
import sys
import venv
import argparse

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error details: {e}")
        sys.exit(1)

def setup_conda_env():
    run_command("conda env create -f environment.yml")
    run_command("conda activate comment_sentiment")
    run_command("pip install -r requirements.txt")

def setup_venv():
    venv.create("venv", with_pip=True)
    if sys.platform == "win32":
        venv_python = os.path.join("venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join("venv", "bin", "python")
    run_command(f"{venv_python} -m pip install --upgrade pip")
    run_command(f"{venv_python} -m pip install -r requirements.txt")

def main(use_conda):
    if use_conda:
        print("Setting up Conda environment...")
        setup_conda_env()
    else:
        print("Setting up virtual environment...")
        setup_venv()

    # Download Stanford CoreNLP models
    run_command("python StanfordNLPCore_Models_dL_install.py")

    # Create necessary directories
    os.makedirs("stanford-corenlp-4.5.7", exist_ok=True)

    # Create .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("ANTHROPIC_API_KEY=your_anthropic_api_key_here\n")
        print("Created .env file. Please fill in your API keys.")

    print("Setup completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup script for Comment Sentiment Analysis project")
    parser.add_argument("--conda", action="store_true", help="Use Conda for environment setup")
    args = parser.parse_args()
    main(args.conda)