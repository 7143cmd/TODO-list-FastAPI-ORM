from db import DATABASE_CONNECT, INSERT_INTO
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
    conn = DATABASE_CONNECT()
    cur = conn.cursor()
    cur.execute("SELECT * FROM passWRD WHERE UserLogin = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user is not None


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):

    conn = DATABASE_CONNECT()
    cur = conn.cursor()
    cur.execute("SELECT * FROM passWRD WHERE UserLogin = ?", (username,))
    user = cur.fetchone()
    conn.close()
  

    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect login or password"
        })
    try:
        decrypted_password = decode_password(user["CachedPassword"])
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
    INSERT_INTO(UserPassword=password, CachedPassword=encrypted_password, UserLogin=username)

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
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("main.html", {"request": request, "username": username})


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("username")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)