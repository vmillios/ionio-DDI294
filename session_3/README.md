# Streamlit Backend (Docker)

This folder contains a minimal Streamlit app and a Dockerfile to run it.

Build the Docker image (run from this folder):

```zsh
docker build -t streamlit-app .
```

Run the container (maps port 8501):

```zsh
docker run --rm -p 8501:8501 streamlit-app
```

Then open http://localhost:8501 in your browser.

Notes:
- The `requirements.txt` currently pins Streamlit to a >=1.22,<2.0 range. Adjust as needed.
- If your app uses additional packages, add them to `requirements.txt` before building the image.
- If you prefer not to use Docker, run locally with:

```zsh
python -m pip install -r requirements.txt
streamlit run main.py
```
