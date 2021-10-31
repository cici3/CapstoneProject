import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils.validation import check_is_fitted

# define a Gaussain NB classifier
clf = MultinomialNB()
model_path = './trainedmodel/newsclassfier_model.pkl'

# # define the class encodings and reverse encodings
# classes = {0: "Class_0", 1: "Class_1", 2: "Class_2"}
# r_classes = {y: x for x, y in classes.items()}


# function to load the model
def load_model():
    global clf
    clf = pickle.load(open(model_path, "rb"))
    if clf is None : print ("clf is none")
    else: print("clf is not none", clf)
  
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
