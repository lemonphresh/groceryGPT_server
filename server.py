import openai
import requests
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from completionPrompt import *
from flask_cors import CORS

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
jwt_secret = os.getenv("JWT")
graphql_url = os.getenv("GRAPHQL_URL")

import sys

print(sys.executable)


app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/update-recipe-name", methods=["POST"])
def update_recipe_name():
    if not request.json: 
        abort(400)
    
    query = """
        mutation UpdateRecipeName($name: String, $recipeId: ID!, $userId: ID!) {
            updateRecipeNameInput(name: $name, recipeId: $recipeId, userId: $userId) {
                id
                name
                link
            }
        }
    """

    data = { "query": query, "variables": request.json }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)

    if not r.json()['data']['updateRecipeName'] and r.json()['data']['updateRecipeName'] != []:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['updateRecipeName']

@app.route("/create-recipe", methods=["POST"])
def create_recipe():
    if not request.json: 
        abort(400)
    
    query = """
        mutation CreateRecipe($createRecipeInput: CreateRecipeInput) {
            createRecipe(createRecipeInput: $createRecipeInput) {
                id
                name
                link
            }
        }
    """

    data = { "query": query, "variables": { "createRecipeInput": request.json } }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)

    if not r.json()['data']['createRecipe'] and r.json()['data']['createRecipe'] != []:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['createRecipe']

@app.route("/delete-recipe", methods=["POST"])
def delete_recipe():
    if not request.json: 
        abort(400)
    
    query = """
        mutation DeleteRecipe($deleteRecipeInput: DeleteRecipeInput) {
            deleteRecipe(deleteRecipeInput: $deleteRecipeInput)
        }
    """

    data = { "query": query, "variables": { "deleteRecipeInput": request.json } }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)

    if not r.json()['data']['deleteRecipe']:
        return jsonify({ 'errors':  r.json()['data']['errors'] })
    
    return r.json()['data']['deleteRecipe']


@app.route("/get-user-recipes", methods=["POST"])
def get_user_recipes():
    if not request.json: 
        abort(400)
    
    query = """
        query GetRecipesByUser($userId: ID!) {
            getRecipesByUser(userId: $userId) {
                id
                name
                link
                createdAt
            }
        }
    """

    data = { "query": query, "variables": request.json }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)

    if not r.json()['data']['getRecipesByUser'] and r.json()['data']['getRecipesByUser'] != []:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['getRecipesByUser']


@app.route("/get-user-ingredients", methods=["POST"])
def get_user_ingredients():
    if not request.json: 
        abort(400)
    
    query = """
        query GetIngredientsByUser($userId: ID!) {
            getIngredientsByUser(userId: $userId) {
                name
            }
        }
    """

    data = { "query": query, "variables": request.json }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)

    if not r.json()['data']['getIngredientsByUser'] and r.json()['data']['getIngredientsByUser'] != []:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['getIngredientsByUser']


@app.route("/update-user-ingredients", methods=["POST"])
def update_user_ingredients():
    if not request.json: 
        abort(400)
    
    query = """
        mutation EditUserIngredients($editUserIngredientsInput: EditUserIngredientsInput) {
            editUserIngredients(editUserIngredientsInput: $editUserIngredientsInput) {
                name
            }
        }
    """

    variables = { "editUserIngredientsInput": request.json }
    data = { "query": query, "variables": variables }
    headers = {"Content-Type": "application/json"}

    r = requests.post(graphql_url
                      , json=data, headers=headers)
    
    if not r.json()['data']['editUserIngredients'] and r.json()['data']['editUserIngredients'] != []:
        return jsonify({ 'errors':  r.json()['errors'] })
    
    return r.json()['data']['editUserIngredients']


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

    r = requests.post(graphql_url
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
    print(request.json)
    variables = { 'loginInput': request.json }
    data = { "query": query, "variables": variables }
    headers = {"Content-Type": "application/json"}
    
    r = requests.post(graphql_url, json=data, headers=headers)

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
