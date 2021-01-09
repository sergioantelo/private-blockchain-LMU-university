from flask import Flask,render_template, redirect, request
import requests
import datetime
import json
import sys

##########
#FELIX
######
# Before package structre, with importing the app variable from the app folder, and calling app.run here, and having
# the application code (view) in separate file. Probably there was a reason, but so far it works this way too and is maybe more intuitive
###### 


app = Flask(__name__)
CONNECTED_NODE_ADDRESS = ""
posts = []
    
  
def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    fetch_posts()
    return render_template('index.html',
                           title='YourNet: Decentralized '
                                 'content sharing',
                           posts=posts,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

##########
#FELIX
##########
if __name__=="__main__":
    blockchain_node = sys.argv[1]
    host_node = sys.argv[2]
    CONNECTED_NODE_ADDRESS = "http://127.0.0.1:"+blockchain_node
    app.run(debug=True,port=host_node)