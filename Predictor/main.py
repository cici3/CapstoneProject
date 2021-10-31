import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from utils import load_model, predict

from fastapi.middleware.cors import CORSMiddleware

# defining the main app
app = FastAPI(title="NewsArticleClassifier", docs_url="/")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# class which is expected in the payload
class QueryIn(BaseModel):
    news_text: str

# class which is returned in the response
class QueryOut(BaseModel):
    news_category: str
   

# Route definitions
@app.get("/ping")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"ping": "pong"}

@app.post("/predict_newscategory", response_model=QueryOut, status_code=200)
# Route to do the prediction using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the news category predicted (200)
def predict_newscategory(query_data: QueryIn):
    print("query in :", QueryIn)
    output = {"news_category": predict(query_data)}
    return output

@app.post("/reload_model", status_code=200)
# Route to reload the model from file
def reload_model():
    load_model()
    output = {"detail": "Model successfully loaded"}
    return output

@app.get("/static",response_class=FileResponse)
async def NewsArticleClassifier():
    return FileResponse("./static/main.html")

# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
