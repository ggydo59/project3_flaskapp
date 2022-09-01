from flask import Flask, render_template, request, Blueprint


pre_bp = Blueprint('prepare', __name__, url_prefix='/prepare')

@pre_bp.route('/')
def index():
    return render_template('prepare.html')
