import uvicorn
from database.core import Session
from database.crud import add_user, get_all_users
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory='templates')
session = Session()


class UserFormData(BaseModel):
    username: str
    email: str
    password: str


@app.get('/', response_class=HTMLResponse, name='users_page')
async def show_users_page(request: Request):
    users = templates.TemplateResponse(
        'index.html',
        {'request': request, 'users': get_all_users(session)},
    )

    return users


@app.post('/', response_class=HTMLResponse)
async def add_user_form(request: Request, form_data: UserFormData = Form(...)):
    user_data = form_data
    add_user(session, user_data.model_dump())

    url = request.url_for('users_page')
    return RedirectResponse(url=url, status_code=303)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
