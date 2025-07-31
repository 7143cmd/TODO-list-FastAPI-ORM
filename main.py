from db import DATABASE_CONNECT_USERS, DATABASE_CONNECT_RECORDS, REGISTRATION_INSERT, Get_USER, ADD, Get_Records, Records
from CacheProcess import decode_password, encrypt_password
from fastapi import *
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


def AlreadyExist(username):
    user = Get_USER(username)
    return user


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    username = request.cookies.get("username")
    if username:
        return RedirectResponse(url="/profile", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):

    user = Get_USER(username)

    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect login or password"
        })
    try:
        decrypted_password = decode_password(user.CachedPassword)
        if password != decrypted_password:
            # print(decrypted_password)
            # print(user)
            # print(password)
            raise ValueError("Wrong Password")
            
    except Exception:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect login or password"
        })
    
    response = RedirectResponse(url="/my_list", status_code=302)
    response.set_cookie("username", username)
    return response

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=HTMLResponse)
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if AlreadyExist(username):
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь уже существует"  
        })

    encrypted_password = encrypt_password(password)
    REGISTRATION_INSERT(UserPassword=password, CachedPassword=encrypted_password, UserLogin=username)

    response = RedirectResponse(url="/login", status_code=302)
    return response


@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("profile.html", {"request": request, "username": username})
    

@app.get("/my_list", response_class=HTMLResponse)
def profile(request: Request):
    # t = 'Work'
    # c = 'Don`t forget'
    # ADD(Username=(request.cookies.get("username")),title=t, context=c )
    # ######################################
    # # print(request.cookies.get("username"))
    # #######################################

    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    records = Get_Records(username)
    
    return templates.TemplateResponse("main.html", {
        "request": request, 
        "username": username,
        "records": records
    })

@app.get("/todo/{record_id}", response_class=HTMLResponse)
def view_record(request: Request, record_id: int):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    session = DATABASE_CONNECT_RECORDS()
    try:
        record = session.query(Records).filter(Records.id == record_id, Records.UserLogin == username).first()
        if not record:
            return RedirectResponse(url="/my_list", status_code=303)
            
        return templates.TemplateResponse("todo_detail.html", {
            "request": request,
            "record": record
        })
    finally:
        session.close()

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("username")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)