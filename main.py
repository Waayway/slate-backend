from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from db import get_db, crud
import datetime
import GETurls
import POSTurls
import DELETEurls
from auth import createUrls
import markdown

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
