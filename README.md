### Server for GroceryGPT

Run `pipenv shell`.
Run `pipenv install --dev`.

You're gonna wanna generate your own [OpenAI](https://openai.com/) API key because I'm too poor to have a team one.

Once you have that key, run `echo 'OPENAI_API_KEY=[your_api_key]' > .env` in the root of the project directory.

Finally, run `python server.py` to start.
