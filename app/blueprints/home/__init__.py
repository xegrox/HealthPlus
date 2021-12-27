from flask import Blueprint, render_template

blueprint = Blueprint(
    'home', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)


@blueprint.route('/')
def home():
    return render_template('index.html')
