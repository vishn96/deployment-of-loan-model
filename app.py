
import os
from flask import Flask, render_template,session, redirect, url_for, session
import pickle
from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, FloatField, TextField,SubmitField, RadioField
from wtforms.validators import DataRequired,NumberRange
import numpy as np 
import joblib

def return_prediction(model,scaler,sample_json):
 
   Age = sample_json['Age']
   Experience = sample_json['Experience']
   Income = sample_json['Income']
   CCAvg = sample_json['CCAvg']
    
   loan = [[Age,Experience, Income, CCAvg]]
   loan = scaler.transform(loan)
   classes = np.array(['No loan', 'Loan'])
   class_ind = model.predict(loan)
 
   return classes[class_ind][0]

app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'someRandomKey'


# REMEMBER TO LOAD THE MODEL AND THE SCALER!
loan_model = joblib.load("model.h5")
loan_scaler = joblib.load("scaler.pkl")

# Now create a WTForm Class
class LoanForm(FlaskForm):
   Age = TextField('Age')
   Experience = TextField('Experience')
   Income = TextField('Income')
   CCAvg =TextField('CCAvg')
   submit = SubmitField('Analyze')
 
    
@app.route('/', methods=['GET', 'POST'])
def index():
  # Create instance of the form.
  form = LoanForm()
  # If the form is valid on submission
  if form.validate_on_submit():
  # Grab the data from the input on the form.
    # Grab the data from the input on the form.
     session['Age'] = form.Age.data
     session['Experience'] = form.Experience.data
     session['Income'] = form.Income.data
     session['CCAvg'] = form.CCAvg.data
     return redirect(url_for("prediction"))
 
  return render_template('home.html', form=form)


@app.route('/prediction')
def prediction():
 #Defining content dictionary
   content = {}
   content['Age'] = float(session['Age'])
   content['Experience'] = float(session['Experience'])
   content['Income'] = float(session['Income'])
   content['CCAvg'] = float(session['CCAvg']) 
   results = return_prediction(model=loan_model,scaler=loan_scaler,sample_json=content)
   return render_template('prediction.html',results=results)



if __name__ == '__main__':
 app.run(debug=True)