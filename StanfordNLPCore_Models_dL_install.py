import stanfordnlp
import os

# Check if the models are already downloaded
models_dir = os.path.expanduser('~/stanfordnlp_resources')
en_model_dir = os.path.join(models_dir, 'en_ewt_models')

if os.path.exists(en_model_dir):
    print("Stanford CoreNLP English models are already downloaded.")
else:
    print("Downloading Stanford CoreNLP English models...")
    stanfordnlp.download('en')
    print("Download complete.")