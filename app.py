
import os
from flask import Flask, render_template
import pickle
from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, FloatField, SubmitField, RadioField
from wtforms.validators import DataRequired


app = Flask(__name__)
# Configure a secret SECRET_KEY
app.config['SECRET_KEY'] = 'qwerty1258'

def return_prediction(model,scaler,encoder,sample_json):
 
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
   Education = sample_json['Education']
 
   loan = [[Age,Experience, Income, CCAvg, Mortgage, Securities_Account,
            CD_Account, Online, CreditCard, Family,Education]]
   
   loan = scaler.transform(loan)
   loan=encoded_df.transform(loan)
   class_ind = model.predict(loan)
 
   return classes[class_ind][0]


# Now create a WTForm Class
class LoanForm(FlaskForm):
   Age = TextField('Age')
   Experience = TextField('Experience')
   CCAvg =TextField('Age')
   Mortgage = TextField('Age')
   Securities_Account = BooleanField('Securities_Account? ')
   CD_Account = BooleanField('CD_Account? ')
   Online = BooleanField('Online? ')
   CreditCard = BooleanField('CreditCard? ')
   Family = RadioField('Family',validators=[DataRequired()], choices=['1', '2','3','4'])
   Education = RadioField('Education',validators=[DataRequired()], choices=['Undergrad', 'Graduate','Advanced/Professional'])
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
   content['CCAvg'] = float(session['CCAvg'])
   content['Mortgage'] = float(session['Mortgage'])
   content['Securities_Account'] = session['Securities_Account']
   content['CD_Account'] = session['CD_Account']
   content['Online'] = session['Online']
   content['CreditCard'] = session['CreditCard']
   content['Family'] = session['Family']
   content['Education'] = session['Education']   
 
   results = return_prediction(model=model,scaler=scaler,encoder=encoded_df,sample_json=content)
   return render_template('prediction.html',results=results)



if __name__ == '__main__':
 app.run(debug=True)