from fastapi.templating import Jinja2Templates
from fastapi import FastAPI


app = FastAPI(title="Chatt", debug=True)



@app.post("/message/<chat_id>")
