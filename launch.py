from App.main import app

# from .App.Services.load_model import load_model

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)