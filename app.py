from flask import Flask, request, render_template, send_file
from flask import Response
import docx2txt as d2t
import pytesseract
from PIL import Image
import pandas as pd
import os
import re


app = Flask(__name__)

# Landing Page
@app.route("/", methods=['GET'])
def home():
    return render_template('landingPage.html')

# @app.route("/textSearcher", methods=['GET'])
# def doc_text_search():
#     return render_template('docTextSearch.html')



# @app.route("/productSearch", methods=['GET'])
# def product_detail():
#     return render_template('productDetail.html')


# Product Search Page
@app.route("/productSearch", methods=['GET','POST'])
def product_searcher():
    try:
        if request.method == 'POST':
            t = request.form["productID"]
            df = pd.read_excel("db_files/products.xlsx")
            print(df.columns)
            df = df[df['id']==t]
            result=[]
            if len(df):
                result.append(f"""Product ID = {df["id"].iloc[0]}""")
                result.append(f"""Product Status = {df["status"].iloc[0]}""")
                result.append(f"""Product Price = {df["price"].iloc[0]}""")
            else:
                result.append(f"No Product Present with ID = {t}")
            return render_template('result.html', data=result)
        elif request.method == 'GET':
            return render_template('productDetail.html')

    except Exception as e:
        return render_template('error.html', message=str(e))


# Dic Text Search Page
@app.route("/textSearcher", methods=['POST', 'GET'])
def text_searcher():
    try:
        if request.method == 'POST':

            t = request.form["textSearch"]
            f = request.files['file']
            filename = f.filename
            file_path = os.path.join('temp_file', filename)
            image_dir = "images"
            f.save(file_path)

            text = d2t.process(file_path, "./images/")
            text_list = text.split("\n")
            image_text_list = []
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

            for i, image_file in enumerate(os.listdir(image_dir)):
                if image_file.endswith('.png'):
                    image_path = os.path.join(image_dir, image_file)                 
                    img = Image.open(image_path)
                    img_text = pytesseract.image_to_string(img)
                    img_text = img_text.split("\n")
                    os.remove(image_path)
                    image_text_list+=(img_text)
            
            text_list = image_text_list+text_list
            result = []
            for sentence in text_list:
                if re.search(t, sentence):
                    result.append(sentence)

            os.remove(file_path)
            return render_template('result.html', data=result)

        elif request.method == 'GET':
            return render_template('docTextSearch.html')
    except Exception as e:
        return render_template('error.html', message=str(e))


if __name__ == "__main__":
    app.run()