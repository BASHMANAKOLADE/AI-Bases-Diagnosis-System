from flask import Flask, render_template, request, redirect, url_for, session
# from langchain.llms import OpenAI
from langchain_openai import OpenAI
import os
from langchain.prompts import PromptTemplate
import re
import markdown
from langchain_google_genai import ChatGoogleGenerativeAI


# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
# os.environ["OPENAI_API_KEY"] = "sk-proj-XgqEa2sW0HPbvxdS9fInT3BlbkFJJdU4B9l8nFiXThLhu56z"
# llm = OpenAI(temperature=0.9)

os.environ["GOOGLE_API_KEY"] = "AIzaSyDvxMfiFrVfx7uT6R7dQ8d4_RS4ykSJ550"
llm = ChatGoogleGenerativeAI(model="gemini-pro")

database = {'GeeksForGeeks': '123',
            'Abdul Kalam': 'xyz', 
            'jony@jony.com': 'abc', 'Tony': 'pqr'}

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


def login_required(f):
    def wrapper(*args, **kwargs):
        print(session.get('logged_in'))
        if not session.get('logged_in', False):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['password']
        database[email] = pwd
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['password']
        if email not in database:
            return render_template('login.html', 
                                info='Invalid User ????!')
        else:
            if database[email] != pwd:
                return render_template('login.html', 
                                    info='Invalid Password ????!')
            else:
                session['logged_in'] = True
                session['email'] = email
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required        
def search():
    if request.method == 'POST':
        return redirect(url_for('result.html'))
    else:
        return render_template('search.html')

@app.route('/result.html')
@login_required
def result():
    age = request.args.get('age')
    gender = request.args.get('gender')
    mainSymptom = request.args.get('mainSymptom')
    symptomStartDate = request.args.get('symptomStartDate')
    fever = request.args.get('fever')
    temperature = request.args.get('temperature')
    cough = request.args.get('cough')
    soreThroat = request.args.get('soreThroat')
    shortnessOfBreath = request.args.get('shortnessOfBreath')
    nasalCongestion = request.args.get('nasalCongestion')
    muscleAches = request.args.get('muscleAches')
    fatigue = request.args.get('fatigue')
    nausea = request.args.get('nausea')
    headache = request.args.get('headache')
    rash = request.args.get('rash')
    contactWithSick = request.args.get('contactWithSick')
    travelHistory = request.args.get('travelHistory')
    workplace = request.args.get('workplace')
    vaccinations = request.args.get('vaccinations')
    chronicConditions = request.args.get('chronicConditions')
    

    # Create a prompt for the LLM
    prompt = PromptTemplate(
        input_variables=[
            "age", "gender", "mainSymptom", "symptomStartDate", "fever", "temperature",
            "cough", "soreThroat", "shortnessOfBreath", "nasalCongestion", "muscleAches",
            "fatigue", "nausea", "headache", "rash", "contactWithSick", "travelHistory",
            "workplace", "vaccinations", "chronicConditions"
        ],
        template="""
        The patient is a {age} year old {gender}. They have reported the following primary symptom: {mainSymptom}, which started on {symptomStartDate}.
        Additional symptoms include:
        - Fever: {fever} (Temperature: {temperature})
        - Cough: {cough}
        - Sore Throat: {soreThroat}
        - Shortness of Breath: {shortnessOfBreath}
        - Nasal Congestion: {nasalCongestion}
        - Muscle Aches: {muscleAches}
        - Fatigue: {fatigue}
        - Nausea: {nausea}
        - Headache: {headache}
        - Rash: {rash}
        
        Exposure history includes:
        - Contact with sick individuals: {contactWithSick}
        - Recent travel history: {travelHistory}
        - Workplace exposure: {workplace}
        
        Medical history includes:
        - Up-to-date with vaccinations: {vaccinations}
        - Chronic conditions: {chronicConditions}
        
        Based on these information, what is the most likely diagnosis and also recommend first aid to be done before getting to hospital?
        """
    )

    # Invoke the LLM with the formatted prompt
    result = llm.invoke(prompt.format(
        age=age, gender=gender, mainSymptom=mainSymptom, symptomStartDate=symptomStartDate,
        fever=fever, temperature=temperature, cough=cough, soreThroat=soreThroat,
        shortnessOfBreath=shortnessOfBreath, nasalCongestion=nasalCongestion, muscleAches=muscleAches,
        fatigue=fatigue, nausea=nausea, headache=headache, rash=rash, contactWithSick=contactWithSick,
        travelHistory=travelHistory, workplace=workplace, vaccinations=vaccinations, chronicConditions=chronicConditions
    ))
    html = markdown.markdown(result.content)

    return render_template('result.html', result = html)
    

if __name__ == '__main__':
    app.run(port=8000, debug=True)
