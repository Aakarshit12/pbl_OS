from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '../pbl_OS/performance_log.csv')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    data = []
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Remove None keys or empty keys
                cleaned_row = {k: v for k, v in row.items() if k is not None and k != ''}
                # Skip empty or malformed rows
                if cleaned_row:
                    data.append(cleaned_row)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
