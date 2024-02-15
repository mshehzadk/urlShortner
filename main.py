import random
import string
import json

from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

shortened_urls = {}

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(length))
    return short_url

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url()
        
        while short_url in shortened_urls:
            short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        with open('urls.json','w') as file:
            json.dump(shortened_urls, file)
        
        return f"Shortened URL: {request.host_url}{short_url}"
    return render_template('index.html')        
    

@app.route('/<short_url>')
def redirect_to_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return f"URL for {short_url} not found", 404
    
if __name__ == '__main__':
    with open('urls.json','r') as file:
        shortened_urls = json.load(file)
    app.run(debug=True)