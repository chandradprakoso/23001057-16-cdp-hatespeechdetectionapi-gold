import re
import pandas as pd

from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)


swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing and Modeling'),
    },
    host= LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    'static_url_path': "/flasgger_static",
    'swagger_ui': True,
    'specs_route': "/docs/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

def cleansing(sent):
    # Mengubah kata menjadi huruf kecil semua dengan menggunakan fungsi lower()
    string = str(sent).lower()
    # Menghapus emoticon dan tanda baca menggunakan "RegEx" dengan script di bawah
    string = re.sub(r'[^a-zA-Z0-9]', ' ', string)
    return string

# Setelah selesai mendefinisikan fungsi "cleansing", selanjutnya kita aplikasikan ke dalam kolom text pada DataFrame
# Caranya menjalankan script di bawah
# data['text_clean'] = data['Text Tweet'].apply(cleansing)

# app = Flask(__name__)

@swag_from("docs/filepostmethod.yml", methods = ['POST'])
@app.route('/', methods=['POST'])
def text_processing():

    text = request.files['file']
    text_clean = pd.read_csv(text, encoding='ISO-8859-1')
    text_clean = text_clean.to_json()
    

    json_response = {
        'status_code': 200,
        'description': "Teks yang skudah diproses",
        'data_raw': text,
        'data_clean': text_clean
    }
    response_data = jsonify(json_response)
    return response_data

'''
def index():
    if request.method == 'GET':
        return render_template('/Users/chandra/Documents/BINAR_DSC_ENV/.venv/templates/upload.html')
    elif request.method == 'POST':
        csv_file = request.files.get('file')
        X_test = pd.read_csv(csv_file, encoding='ISO-8859-1')
        # data['Tweet_clean'] = data['Tweet'].apply(cleansing)
        X_test['Cleaned'] = X_test['Tweet'].apply(cleansing)
        X_html = X_test.to_html()

        return X_html
    '''
    
if __name__ == '__main__':
    app.run(debug=True)