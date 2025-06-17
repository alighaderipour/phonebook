python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
cd backend
python run.py


cd frontend
npm install
npm install vue-router@4
npm install pinia
