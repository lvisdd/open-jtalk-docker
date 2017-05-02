from flask import Flask
from flask import jsonify, render_template, request
from janome.tokenizer import Tokenizer
import urllib.parse

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.route('/tokenizer', methods=['GET', 'POST'], strict_slashes=False)
def tokenizer():
    if request.method == 'POST':
        question = request.form['question']
        
    else:
        question = request.args.get('question')
    
    # print(urllib.parse.unquote(question))
    
    t = Tokenizer()
    try:
      tokendata = t.tokenize(urllib.parse.unquote(question))
    except:
      return question
    
    words=[]
    for token in tokendata:
      words.append(token.surface)
    
    print(" ".join(words))
    # question=" ".join(words)
    
    # if request.method == 'POST':
    #   return jsonify(" ".join(words))
    # else:
    return jsonify(" ".join(words))

if __name__ == '__main__':
  app.run()
