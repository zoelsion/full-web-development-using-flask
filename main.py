from flask import Flask,render_template,flash, url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder.charts.views import DirectByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg
from flask import jsonify, request, render_template


app = Flask (__name__)

@app.route('/')
def index():
   return render_template('child.html')


if __name__ == '__main__':

   app.run(debug = True)