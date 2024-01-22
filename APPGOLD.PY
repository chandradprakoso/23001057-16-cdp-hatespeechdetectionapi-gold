from flask import Flask, render_template, request, jsonify, send_file
from flasgger import Swagger
import pandas as pd
import io
import re

app = Flask(__name__)
Swagger(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    Upload a CSV file, clean it, and download the cleaned CSV file.

    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The CSV file to be cleaned.

    responses:
      200:
        description: The cleaned CSV file.
    """
    file = request.files['file']
    if file:
        try:
            # Read CSV file into a Pandas DataFrame
            file_contents = file.read().decode('latin1')
            df = pd.read_csv(io.StringIO(file_contents))

            # Perform cleaning using regular expressions (you can customize this part)
            df = clean_data(df)

            # Save cleaned DataFrame to CSV
            cleaned_csv = io.StringIO()
            df.to_csv(cleaned_csv, index=False)
            cleaned_csv.seek(0)

            return send_file(
                cleaned_csv,
                mimetype='text/csv',
                as_attachment=True,
                download_name='cleaned_data.csv'
            )
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'No file uploaded'})

def clean_data(df):
    # Example: Remove non-alphanumeric characters from column names
    df.columns = [re.sub(r'\W', '_', col) for col in df.columns]

    # Add your custom data cleaning logic here using Pandas and regex
    # For example, you can remove NaN values, convert data types, etc.

    return df

if __name__ == '__main__':
    app.run(debug=True)
