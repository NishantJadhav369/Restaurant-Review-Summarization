from flask import Flask,request,render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    dish = request.args.get('dish_name')
    review = []
    rev = pd.read_excel("NVA_PHRASE_SENTIMENT_215.xlsx")
    '''
    phr = list(rev['phrase'])
    hotel = list(rev['hotel'])
    phrase_hotel_dict = {}
    for i,j in zip(phr,h) :
        if dish in i :
            if j in phrase_hotel_dict :
                phrase_hotel_dict[j].append(i)
            else :
                phrase_hotel_dict[j] = [i]
    '''
    return render_template('food.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    name = request.args.get('name')
    password = request.args.get('password')
    return render_template('profile.html',name=name)

@app.route('/restaurant')
def restaurant():
    rest_name = request.args.get('rest_name')

    review = []
    df = pd.read_excel("NVA_PHRASE_SENTIMENT_215.xlsx")
    df['hotel'] = df['hotel'].apply(lambda s : s.lower())
    #phrase_list = list(rev[rev['hotel'] == rest_name.lower() ]['phrase'])

    rev = df[df['hotel']==rest_name].sort_values('polarity',ascending=False)
    phrase_list = list(rev['phrase'])
    polarity_list = list(rev['polarity'])
    length = len(phrase_list)

    return render_template('restaurant.html',rest_name=rest_name,phrase_list=phrase_list,polarity_list=polarity_list,length = length)


if __name__ == "__main__":
	app.run(debug=True)
