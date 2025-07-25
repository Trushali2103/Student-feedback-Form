from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

EXCEL_FILE = 'feedback_data.xlsx'

COLUMNS = ['Name', 'Email', 'Course', 'Year', 'Rating', 'Feedback', 'Suggestions', 'Timestamp']

# Route to serve the HTML file
@app.route('/')
def serve_index():
    return send_from_directory('', 'aindex.html')  # Make sure 'index.html' is in the same folder as app.py

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()

        # Check for required fields
        required_fields = ['name', 'email', 'course', 'year', 'rating', 'feedback', 'suggestions']
        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return jsonify({'success': False, 'message': f'Missing fields: {", ".join(missing)}'}), 400

        # Prepare new data row
        new_row = {
            'Name': data['name'],
            'Email': data['email'],
            'Course': data['course'],
            'Year': data['year'],
            'Rating': data['rating'],
            'Feedback': data['feedback'],
            'Suggestions': data['suggestions'],
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Load existing Excel
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
        else:
            df = pd.DataFrame(columns=COLUMNS)

        # Append and save
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
