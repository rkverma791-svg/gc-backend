from flask import Flask

print("🔥 APP LOADED SUCCESSFULLY")

app = Flask(__name__)

@app.route('/')
def home():
    return "WORKING OK"

@app.route('/test')
def test():
    return "TEST OK"

@app.route('/ping')
def ping():
    return "SERVER RUNNING"

# IMPORTANT FOR RENDER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
