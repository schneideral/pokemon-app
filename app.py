from flask import Flask, request, jsonify, render_template
from service import MonService

import json
import requests
import os


app = Flask(__name__)


@app.after_request
def add_headers(response):
   response.headers['Access-Control-Allow-Origin'] = "*"
   response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
   response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
   return response


@app.route("/", methods=['GET', 'POST'])
def add_pokemon():
    #if request.method == 'POST':
     #   name = request.form['name']
      #  moves = request.form.getlist('moves')
       # new_pokemon = {
        #    "pokemon": name,
         #   "moves": moves
       # }
       # try:
        #    response = requests.post("http://docker.internal.host:5000/todo", json=new_pokemon, timeout=5)
       # except requests.exceptions.RequestException as e:
        #    print('Failed to add todo item: {e}')
         #   return "Failed", 404
    return render_template('add_pokemon.html')


@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(MonService().list())


@app.route("/todo", methods=["POST"])
def create_todo():
    data = None
    if request.content_type == 'application/x-www-form-urlencoded':
        im = request.form
        data = {}
        for key, value in im.items():
            if key not in data:
                data[key] = value
            elif isinstance(data[key], list):
                data[key].append(value)
            else:
                data[key] = [data[key], value]
    elif request.content_type == 'application/json':
        data = request.get_json()
    else:
        return "Unsupported Media Type", 415
    print(data)
    return jsonify(MonService().create(data))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(MonService().update(item_id, request.get_json()))


@app.route("/todo/<item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify(MonService().get_by_id(item_id))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(MonService().delete(item_id))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8888)))

