import os

from livereload import Server
from app import app

if __name__ == '__main__':
    if os.environ.get('DEBUG') == "1":
        app.debug = True
        server = Server(app.wsgi_app)
        server.serve(host='0.0.0.0', liveport=35729)
    else:
        app.run(host='0.0.0.0')
