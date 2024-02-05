python -m venv .venv

source .venv/bin/activate (Linux/Mac)
or .venv/Scripts/activate (Windows)

pip install -r requirements.txt

python src/download_resources.py

streamlit run app.py