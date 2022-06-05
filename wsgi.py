from consumer import app

# production specific settings
app.config['DEBUG'] = False
app.config['ENV'] = 'production'
