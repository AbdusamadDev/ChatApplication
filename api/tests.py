# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# app = FastAPI()

# # Mount the static files directory
# app.mount("/static", StaticFiles(directory="../static"), name="static")

# # Initialize Jinja2 templates
# templates = Jinja2Templates(directory="../templates")

# # Define route to render index.html template
# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})

# # Define route to handle form submission
# @app.post("/submit/")
# async def submit_form(request: Request, data: str = Form(...)):
#     # Handle form submission logic
#     return {"data": data}

# # Run the application using Uvicorn
# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
print("")