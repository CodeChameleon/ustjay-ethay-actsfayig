import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup
import bs4

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_pig_latin(url):
    response = requests.get(url)
    # return response.content
    # soup.find_all("body")
    soup = BeautifulSoup(response.content, "html.parser").find("body")

    # return BeautifulSoup.BeautifulSOAP(response.content).html.find("body", text=True, recursive=False)
    return "".join([t for t in soup.contents if type(t)==bs4.element.NavigableString])
    return soup.find_all("body")[0]

@app.route('/')
def home():
    fact = get_fact();
    payload = { "input_text": fact }
    session = requests.Session()
    response = session.post('https://hidden-journey-62459.herokuapp.com/piglatinize/', 
        data=payload,
        allow_redirects=False)
    url = response.headers['Location']
    pig_latin = get_pig_latin(url)
    result = f"""
<html>
<body>
    <h1>Random Pig-Latin Quote</h1>
    <a target='_blank' href='{url}'>{url}</a>
    <p><b>Fact</b>: {fact}</p>
    <p><b>Pig Latin</b>: {pig_latin}</p>
</body>
</html>
    """
    return result


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

