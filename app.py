
import os
from flask import Flask, render_template,session, redirect, url_for, session
import pickle
from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, FloatField, TextField,SubmitField, RadioField
from wtforms.validators import DataRequired,NumberRange
import numpy as np
import pandas as pd
import joblib

def return_prediction(model,sample_json):
 
   Age = sample_json['Age']
   Experience = sample_json['Experience']
   Income = sample_json['Income']
   CCAvg = sample_json['CCAvg']
   Mortgage = sample_json['Mortgage']
   Securities_Account = sample_json['Securities_Account']
   CD_Account = sample_json['CD_Account']
   Online = sample_json['Online']
   CreditCard = sample_json['CreditCard']
   Family = sample_json['Family']
   Education =sample_json['Education']
    
   loan = [[Age,Experience, Income, CCAvg,Mortgage,Securities_Account,CD_Account,Online,CreditCard,Family,Education]]
   classes = np.array(['No loan', 'Loan'])
   class_ind = model.predict(loan)
 
   return classes[class_ind][0]

app = Flask(__name__)
# Configure a secret SECRET_KEY
# We will later learn much better ways to do this!!
app.config['SECRET_KEY'] = 'someRandomKey'


# REMEMBER TO LOAD THE MODEL AND THE SCALER!
loan_model = joblib.load("model.h5")

# Now create a WTForm Class
class LoanForm(FlaskForm):
   Age = TextField('Age')
   Experience = TextField('Experience')
   Income = TextField('Income')
   CCAvg =TextField('How much is your average Credit Card Spending?')
   Mortgage = BooleanField('Do you have a Mortgage? ')
   Securities_Account = BooleanField('Do you have a Securities Account? ')
   CD_Account = BooleanField('Do you have a CD Account? ')
   Online = BooleanField('Did you register for Online Banking? ')
   CreditCard = BooleanField('Do you have a Credit Card? ')
   Family = RadioField('How many members are there in your family?',choices=[('1','1 Family Member'), ('2','2 Family Members'),('3','3 Family Members'),('4','4+ Family Members')])
   Education = RadioField('Education', choices=[('1','Undergrad'), ('2','Graduate'),('3','Advanced/Professional')])
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
     session['Mortgage'] = form.Mortgage.data
     session['Securities_Account'] = form.Securities_Account.data
     session['CD_Account'] = form.CD_Account.data
     session['Online'] = form.Online.data
     session['CreditCard'] = form.CreditCard.data
     session['Family'] = form.Family.data
     session['Education'] = form.Education.data
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
   content['Mortgage'] = int(session['Mortgage'])
   content['Securities_Account'] = int(session['Securities_Account']) 
   content['CD_Account'] = int(session['CD_Account']) 
   content['Online'] = int(session['Online']) 
   content['CreditCard'] = int(session['CreditCard']) 
   content['Family'] = int(session['Family']) 
   content['Education'] = int(session['Education']) 
   results = return_prediction(model=loan_model,sample_json=content)
   return render_template('prediction.html',results=results)



if __name__ == '__main__':
 app.run(debug=True)
