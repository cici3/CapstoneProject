import pickle
from sklearn import pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils.validation import check_is_fitted
from sklearn.pipeline import Pipeline  as sklearnpipeline

# define a Gaussain NB classifier
clf = MultinomialNB()
model_path = './trainedmodel/newsclassfier_model.pkl'

#added these classes to retrain the model
news_classes = {0:'CRIME' ,1:'ENTERTAINMENT', 2:'WORLD NEWS' ,3:'IMPACT' ,4:'POLITICS', 5:'WEIRD NEWS',6:'BLACK VOICES', 7:'WOMEN' , 8:'COMEDY' , 9:'QUEER VOICES', 10:'SPORTS', 11:'BUSINESS',
 12:'TRAVEL' ,13:'MEDIA', 14:'TECH' ,15:'RELIGION' ,16:'SCIENCE' ,17:'LATINO VOICES', 18:'EDUCATION',19:'COLLEGE' ,20:'PARENTS' ,21:'ARTS & CULTURE' ,22:'STYLE' ,23:'GREEN',24:'TASTE',25: 'HEALTHY LIVING', 26: 'THE WORLDPOST' , 27:'GOOD NEWS', 28:'WORLDPOST' ,29:'FIFTY', 30:'ARTS',31:'WELLNESS' ,32:'PARENTING' ,33:'HOME & LIVING', 34:'STYLE & BEAUTY', 35:'DIVORCE',36:'WEDDINGS' ,37:'FOOD & DRINK' ,38:'MONEY' ,39:'ENVIRONMENT', 40: 'CULTURE & ARTS'}
r_classes = {y: x for x, y in news_classes.items()}


# function to load the model
def load_model():
    global clf 
    clf = pickle.load(open(model_path, "rb"))
    if clf is None : print ("clf is none")
    else: print("clf is not none", clf)
    return clf
  
# function to predict the category using the model
def predict(query_data):
    #x = list(query_data.dict().values())
    load_model()
    print(query_data)
    x = list(query_data.dict().values())
    print("X:",x , type(x))
    #prediction = clf.predict(["medicine test test carona flu"])
    prediction = clf.predict(x)
    print(prediction)
    print(type(prediction))
    prediction = str(prediction)
    return prediction

def categories_for_retraining():
    return news_classes

# function to train and save the model as part of the feedback loop
def retrain_model(data):
    # load the model
    clf = load_model()
    # print(type(clf))
    # pull out the relevant X and y from the FeedbackIn object
    X = [list(d.dict().values())[:-1] for d in data]
    y = [[d.news_category] for d in data]
  
    print(X[0])
    print(y[0])
    # fit the classifier again based on the new data obtained
    (clf).fit(X[0], y[0])
    # save the model
    pickle.dump(clf, open(model_path, "ab"))
