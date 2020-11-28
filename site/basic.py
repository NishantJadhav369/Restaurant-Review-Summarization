from flask import Flask,request,render_template
import pandas as pd

#### PREDICTION PAGE IMPORT STARTS #####
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


#### PREDICTION PAGE IMPORT ENDS #####


app = Flask(__name__)

#### PREDICTION PAGE CODE #####
tag2idx,idx2tag = pickle.load(open('mlfiles/tag2idx_idx2tag_w2v_final2','rb'))
tokenizer = pickle.load(open('mlfiles/tokenizer_w2v_final2','rb'))
model = tf.keras.models.load_model('mlfiles/BILSTM_model_final2.h5')

num_words = len(tokenizer.word_index)
max_len =30
sents = []
tagseq =[]
def give_prediction(text):
    max_len =30
    sents = []
    tagseq =[]
    text = text.lower()
    sentence_ids = tokenizer.texts_to_sequences([text])
    padded_ids = pad_sequences(maxlen=max_len, sequences=sentence_ids, padding="post", value=num_words)
    pred = model.predict(padded_ids)
    pred = np.argmax(pred,axis=-1)
    review_words = text.split()
      # text_padded = tokenizer.sequences_to_texts(sentence_ids)
    c=0
    for i,y in enumerate(pred[0,:]):
    #print(review_words[i],idx2tag[y])
        c+=1
        if c == len(review_words):
            break
        sents.append(review_words[i])
        tagseq.append(idx2tag[y])
        #print(f'{idx2word[x] : {15}} {idx2tag[y] :{15}}')
        #print("{:15}{}\t{}".format(x,y))
    foods=[] #contains individual E
    for i,word in enumerate(zip(sents,tagseq)):
        # print(word)
        #print(word)
        if word[1] == 'E':
            foods.append(word[0])
    dishes= [] # combines bigram E as well
    for i,(word,tag) in enumerate(zip(sents,tagseq)) :
        if i == 0: #first word case only
            if tag == 'E':
                dishes.append(word)
                continue
        if tag=='E':
            dishes.append(word)
            if tagseq[i-1]=='E': #check if previous word is also E
                first = dishes.pop(-2) #remove previous E
                dishes[-1]=first+' '+word # combine both E
    
    return dishes
# text = "The spicy chicken and curry is amazing"
# give_prediction(text)

#### PREDICTION PAGE CODE ENDS #####

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/food')
def food():
    dish = request.args.get('dish_name')
    review = []
    rev = pd.read_csv("NVA_PHRASE_SENTIMENT_215.csv")
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
    rest_name = rest_name.lower()
    review = []
    df = pd.read_csv("NVA_PHRASE_SENTIMENT_215.csv")
    
    df['hotel'] = df['hotel'].apply(lambda s : s.lower())
    #phrase_list = list(rev[rev['hotel'] == rest_name.lower() ]['phrase'])

    rev = df[df['hotel']==rest_name].sort_values('polarity',ascending=False)
    phrase_list = list(rev['phrase'])
    polarity_list = list(rev['polarity'])
    length = len(phrase_list)

    return render_template('restaurant.html',rest_name=rest_name,phrase_list=phrase_list,polarity_list=polarity_list,length = length)


########

@app.route('/predict',methods = ["GET","POST"])
def predict():
    if request.method == "POST" :
        sentence = request.form.get("sentence")
        #uncomment the line below after the function
        sentence = sentence.lower()
        print(sentence)
        food = give_prediction(sentence)
        # food = ['name','xyz'] ## delete this line after uncommenting the above line
        print(sentence.split(),food)



        return render_template('predict_dish.html',food = food,sentence = sentence.split())
    else :
        return render_template('predict_dish.html')

########

if __name__ == "__main__":
	app.run(debug=True)
