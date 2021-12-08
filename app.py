from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import certifi
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from wtforms import (StringField,SubmitField)
from flask_restful import Resource,Api
import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)

api = Api(app)

class User(Resource):
    def get(self,name):
        return {'firstname':name}

api.add_resource(User,'/user/<string:name>')
if __name__ == "__main__":
    app.run(port=5000)

#config a flask form
class MyForm(FlaskForm):
    title = StringField("Please input the task's title:", validators=[DataRequired()])
    content = StringField("Please input the content:",validators=[DataRequired()])
    deadline = StringField("Please input the deadline:",validators=[DataRequired()])
    ttype = SelectField("Please select your task type:", choices=[('urgent', 'urgent'), ('normal', 'normal')])
    country = SelectField("Please select your country:", choices=[('Belfast', 'Belfast'), ('Dublin', 'Dublin'), ('Cork', 'Cork'), ('Galway', 'Galway')])
    submit = SubmitField('Submit')

app.config["MONGO_URI"] = "mongodb+srv://jovy:Jetzuko0429@cluster0.0s51g.mongodb.net/assignment-two?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = "secret_key"

mongo = PyMongo(app, tlsCAFile=certifi.where())

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/add', methods=['GET','POST'])
def add():
    info = MyForm()
    if request.method == 'POST':
        ttype = request.form['ttype']
        title = request.form['title']
        content = request.form['content']
        deadline = request.form['deadline']
        country = request.form['country']

        print(ttype,country,content,deadline,title)

        try:
            mongo.db.jovyy.insert_one({
                'title':title,
                'content':content,
                'deadline':deadline,
                'ttype':ttype,
                'country':country
            })
            return render_template("thankyou.html",ttype=ttype)
        except:
            return "There was an error adding."
    else:
        return render_template("add.html",form=info)

@app.route('/remind')
def remind():
    data = mongo.db.jovyy.find({})
    return render_template('remind.html',data=data)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/chart')
def chart():
    alldata = mongo.db.jovyy.find()
    s_city = []
    for x in range(4):
        s_city.append(int(0))
    n_city = np.array(['Belfast', 'Dublin', 'Cork', 'Galway'])
    all_list = list(alldata)
    for x in all_list:
        if x['country'] == 'Belfast':
            s_city[0] += 1
        if x['country'] == 'Dublin':
            s_city[1] += 1
        if x['country'] == 'Cork':
            s_city[2] += 1
        if x['country'] == 'Galway':
            s_city[3] += 1
    s_city = np.array(s_city)
    plt.bar(n_city, s_city)
    plt.savefig('static/images/chart.jpg')
    plt.show()
    return render_template('chart.html')

