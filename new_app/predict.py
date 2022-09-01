from flask import Flask, render_template, request, Blueprint
import pickle
from movie_crawling import movie_crawl
import numpy as np
import pandas as pd
import time


bp = Blueprint('predict', __name__)

@bp.route('/')
def main():
    return render_template('main.html')


@bp.route('/predict/', methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')
  
@bp.route('/predict/predict_result', methods=['GET', 'POST'])
def predict_result():
    model = None
    # loads = os.getcwd().replace('\\', '//')
    with open('model2.pkl', 'rb') as pickle_files:
        model = pickle.load(pickle_files)
           
    if request.method == 'POST':
        title = request.form['title']
        info = movie_crawl(title)
        time.sleep(2)
        if info == None:
            return render_template('search_fail.html')
        else:
            column = [
                    'title',
                    'years',
                    'ratings',
                    'scores',
                    'votes',
                    'director',
                    'movie_rate',
                    'genre1',
                    'genre2',
                    'lead_actor',
                    'sup_actor']
            movie_info = pd.DataFrame(
                [info[:-1]],
                columns=column)
            res = model.predict(movie_info)
            result = np.exp(res)
            return render_template('predict_result.html', image=info[-1], column=column, info = info[:-1], result=round(result[0],2), title = title)
