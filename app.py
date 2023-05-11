from flask import Flask, request, render_template, send_file
from flask import Response
import docx2txt as d2t
import pytesseract
from PIL import Image
import os
import re


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('index.html')



@app.route("/textSearcher", methods=['POST'])
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

            print(result)
            print("*"*100)
            
            return render_template('result.html', data=text)
    except Exception as e:
        return Response(str(e))


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8001)