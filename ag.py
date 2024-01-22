import pandas as pd
from flask import Flask, render_template, request, jsonify
import jsonpickle
import jsonpickle.ext.pandas as jsonpickle_pandas
import re 

def cleansing(sent):
    # Mengubah kata menjadi huruf kecil semua dengan menggunakan fungsi lower()
    string = str(sent).lower()
    # Menghapus emoticon dan tanda baca menggunakan "RegEx" dengan script di bawah
    string = re.sub(r'[^a-zA-Z0-9]', ' ', string)
    return string

# Setelah selesai mendefinisikan fungsi "cleansing", selanjutnya kita aplikasikan ke dalam kolom text pada DataFrame
# Caranya menjalankan script di bawah
# data['text_clean'] = data['Text Tweet'].apply(cleansing)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        csv_file = request.files.get('file')
        X_test = pd.read_csv(csv_file, encoding='ISO-8859-1')
        # data['Tweet_clean'] = data['Tweet'].apply(cleansing)
        X_test['Cleaned'] = X_test['Tweet'].apply(cleansing)
        X_html = X_test.to_html()

        return X_html
    
if __name__ == '__main__':
    app.run(debug=True)