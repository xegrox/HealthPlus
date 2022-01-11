from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from app.models.account import Staff

blueprint = Blueprint(
    'home', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)


@blueprint.route('/')
def home():
    if isinstance(current_user, Staff):
        return redirect('/dashboard')
    else:
        return render_template('home/index.html')
