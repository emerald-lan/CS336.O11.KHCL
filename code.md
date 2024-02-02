python -m venv .venv

source .venv/bin/activate
or .venv/Scripts/activate

pip install -r requirements.txt

python download_resources.py

streamlit run app.py


