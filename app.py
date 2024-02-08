import logging
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
from flask import Flask,render_template,request
import requests
import os




app = Flask(__name__)


logging.basicConfig(filename='errors.log',level=logging.ERROR, format='%(asctime)s')
save_dir = "images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

@app.route('/',methods=['GET'])
def home():
    try:
        return render_template('home.html')
    except FileExistsError as e:
        logging.error(f'file is not present in our directory {e}')
    
@app.route('/result',methods=['POST'])
def dashboard():
    try:
        if request.method == 'POST':
            query = request.form['name'].replace(' ', "")

            a = []
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response = f"https://www.google.com/search?q={query}&tbm=isch"
            reql = requests.get(response, headers=headers)
            html_data = bs(reql.content, 'html.parser')
            image_data = html_data.find_all('img')
            del image_data[0]

            for index, img_tag in enumerate(image_data):
                img_url = img_tag.get('src')
                if img_url:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        with open(os.path.join(save_dir, f"{query}_{index}.jpg"), "wb") as f:
                            f.write(img_response.content)
                        a.append(f"{query}_{index}.jpg")
                    else:
                        logging.error(f"Failed to download the image from '{img_url}'")

            return render_template('results.html')
    except Exception as e:
        logging.error(f'this is my request error {e}')
    return render_template('results.html')
        
    
if __name__ == '__main__':
    app.run(debug=True)