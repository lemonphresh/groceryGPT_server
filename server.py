import openai
import jwt
import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from completionPrompt import *
from flask_cors import CORS

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
jwt_secret = os.getenv("JWT")
database_url = os.getenv("DATABASE_URL")

import sys

print(sys.executable)


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/register", methods=["POST"])
def register_user():
    if not request.json:
        abort(400)

    query = """
        mutation RegisterUser($registerInput: RegisterInput) {
            registerUser(registerInput: $registerInput)  {
                id
                username
                email
                password
                token
            }
        }
    """    
    variables = {'registerInput': request.json }
    data = { "query": query, "variables": variables }
    headers = {"Content-Type": "application/json"}

    r = requests.post(database_url
                      , json=data, headers=headers)

    if not r.json()['data']['registerUser']:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['registerUser']

@app.route("/login", methods=["POST"])
def login_user():
    if not request.json:
        abort(400)

    query = """
        mutation LoginUser($loginInput: LoginInput) {
            loginUser(loginInput: $loginInput)  {
                id
                username
                email
                password
                token
            }
        }
    """

    variables = { 'loginInput': request.json }
    data = { "query": query, "variables": variables }
    headers = {"Content-Type": "application/json"}
    
    r = requests.post(database_url, json=data, headers=headers)

    if not r.json()['data']['loginUser']:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['loginUser']


@app.route("/chat", methods=["POST"])
def create_chat_completion():
    if not request.json or not "prompt" in request.json:
        abort(400)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": completionPrompt2() },
            { "role": "user", "content": request.json["prompt"] },
        ],
    )
    reply = response.choices[0].message

    return jsonify({ "response": reply.content })


if __name__ == "__main__":
    app.run(debug=True)
