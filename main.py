from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from db import get_db
import GETurls
import POSTurls
import DELETEurls
from auth import createUrls
import markdown
import os

# ### DEVELOPMENT, COMMENT IN ACTUAL USE
# from dotenv import load_dotenv

# load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
# ### DEVELOPMENT COMMENT IN USE

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = get_db()


@app.get("/", response_class=HTMLResponse)
def root():
    html = ""
    with open("README.md", "r") as f:
        nonformat = f.read()
        html = markdown.markdown(nonformat)
    return html


GETurls.addGetRequests(app)
POSTurls.addPostRequests(app)
DELETEurls.addDeleteRequests(app)
createUrls(app)
