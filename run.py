import os

from livereload import Server
from app import app

if __name__ == '__main__':
    if os.environ.get('DEBUG') == "1":
        app.debug = True
        server = Server(app.wsgi_app)
        server.watch('app/templates/*.html')
        server.watch('app/blueprints/**/*.html')
        server.watch('app/static/dist/main.css')
        server.serve(liveport=35729)
    else:
        app.run()
