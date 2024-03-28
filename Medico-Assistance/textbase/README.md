## Start development server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py`.

Run the following command:
cd textbase
poetry env list
poetry show -v
poetry env remove python
poetry install
```bash
poetry run python textbase/textbase_cli.py test main.py
```
Now go to [http://localhost:4000](http://localhost:4000) and start chatting with your bot! The bot will automatically reload when you change the code

poetry self update