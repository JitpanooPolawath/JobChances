from flask import Blueprint, render_template, request, flash
from pred import train_model

views = Blueprint('view', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        Age = request.form.get('Age')
        Accessibility = request.form.get('Accessibility')
        EdLevel = request.form.get('EdLevel')
        Employment = request.form.get('Employment')
        Gender = request.form.get('Gender')
        MentalHealth = request.form.get('MentalHealth')
        YearsCode = request.form.get('YearsCode')
        YearsCodePro = request.form.get('YearsCodePro')
        Salary = request.form.get('Salary')
        Country = request.form.get('Country')
        ComputerSkills = request.form.get('ComputerSkills')


        if int(Age) < 10:
            flash('Age must be older than 10 years old.', category='error')        
        elif Accessibility is None:
            flash('Didn\'t select Accessibility.', category='error')    
        elif EdLevel is None:
            flash('Didn\'t select Education.', category='error')    
        elif Employment is None:
            flash('Didn\'t input Employment.', category='error')    
        elif Gender is None:
            flash('Didn\'t select Gender.', category='error')    
        elif MentalHealth is None:
            flash('Didn\'t select Mental Health..', category='error')    
        elif YearsCode is None:
            flash('Didn\'t input YearsCode.', category='error')
        elif YearsCodePro is None:
            flash('Didn\'t input YearsCodePro.', category='error')
        elif Salary is None:
            flash('Didn\'t input Salary.', category='error')
        elif Country is None:
            flash('Didn\'t select Country.', category='error')
        elif ComputerSkills is None:
            flash('Didn\'t input ComputerSkills.', category='error')
        else:
            Age = int(Age)
            Accessibility = int(Accessibility)
            EdLevel = int(EdLevel)
            Employment = int(Employment)
            Gender = int(Gender)
            MentalHealth = int(MentalHealth)
            YearsCode = int(YearsCode)
            YearsCodePro = int(YearsCodePro)
            Salary = int(Salary)
            Country = int(Country)
            ComputerSkills = int(ComputerSkills)
            prediction = train_model(Age, Accessibility, EdLevel, Employment,
                                                Gender, MentalHealth, YearsCode, YearsCodePro,
                                                Country, Salary, ComputerSkills)
            flash('Information gathered successfully.', category='success')
            return render_template("answer.html", input_string=prediction)
        

    return render_template("home.html")