from typing import Any
from fastapi import FastAPI, Request, Body, WebSocket, WebSocketDisconnect, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import asyncio
from models import gift_for_riddle, auth_check_password,register_password, auth_password,rat_win, auth,get_friends, game_ch,get_profile, rat_auth, referation_system, register, register_name, one_win, get_nickname
import aiofiles
from download import download_avatar
from urllib.parse import unquote
from auth import check_pass
from aiogram.methods.create_invoice_link import CreateInvoiceLink
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot
from aiogram import types

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(name="auth.html", request=request)

@app.post('/')
async def index(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')
    idi = m[1][:m[1].find("&password")]
    pasw = m[-1]
    print(pasw,idi)
    boolean_f = asyncio.create_task(auth_check_password([idi, pasw]))
    return await boolean_f


@app.get('/game')
async def index(request: Request):
    return templates.TemplateResponse(name="start.html", request=request)


@app.post('/game')
async def update_item(payload: Any = Body(None)):
    tok = '6719114253:AAEGvzdBuqPjMbVJtlP_UUYiSbw-uKbeghU'
    bot = Bot(token=tok)
    m = await bot.create_invoice_link("Покупка","Тестовый","true","XTR",prices=[types.LabeledPrice(label='Покупка',amount=1)])
    print(m)
    return {1:m}
    try:
        m = payload.decode('utf-8').split('=')
    except:
        m=''
    idi = m[1].find("&password")
    idi = m[1][:idi]
    boolean = await asyncio.create_task(check_pass([idi, m[-1]]))
    if boolean and len(m)==3:
        if m[0]=='telegramid':
            game_db = asyncio.create_task(game_ch([m[0], idi]))
            return await game_db
        elif m[0]=='telegram':
            auth_db = asyncio.create_task(auth([m[0], idi]))
            return await auth_db
        elif m[0]=='register':
            check_auth = asyncio.create_task(register([m[0], idi]))
            return await check_auth
    return False


@app.get('/rating')
async def indexx(request: Request):
    return templates.TemplateResponse(name="game.html", request=request)


@app.post('/rating') # RETURNING KEY:DATA, WHERE DATA1 = BALANCE, DATA2 = ACCESS TO CHAT(TOP 5)
async def indexxx(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')

    if m[0]=='telegram':
        rat_db = asyncio.create_task(rat_auth(m))
        return await rat_db
    elif m[0]=='winners':
        sel_win = asyncio.create_task(rat_win(m))
        return await sel_win
    elif m[0]=='selectwinner':
        m[1]=unquote(m[1])
        one_win_ = asyncio.create_task(one_win(m))
        return await one_win_
    elif m[0]=='actname':
        get_nick = asyncio.create_task(get_nickname(m))
        return await get_nick
    elif m[0]=='telegramidi':
        idi = m[1].find("&password")
        idi = m[1][:idi]
        get_auth = asyncio.create_task(auth_password([idi, m[-1]]))
        return await get_auth

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/rating")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            await manager.broadcast(f"{data}<br />")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/ref/{user_id}")
async def ref_system(user_id, request: Request):
    return templates.TemplateResponse(name="testing_ref.html", request=request)


@app.post("/ref")
async def ref_system_post(payload: Any = Body(None)):
    m = list(map(lambda x: x.split('='), payload.decode('utf-8').split('&')))
    ref_s = asyncio.create_task(referation_system(m))
    return await ref_s


@app.get("/register")
async def register_user(request: Request):
    return templates.TemplateResponse(name='register.html', request=request)


@app.post("/register")
async def ref_system_post(file: UploadFile):
    down = asyncio.create_task(download_avatar(file))
    return await down


@app.post("/register2")
async def ref_system_post(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')
    if m[0] == 'name':
        m[1]=unquote(m[1])
        m[1] = m[1][:m[1].find('telegramtodelete')-1]
        json = {'nickname':m[1], 'id':m[-1]}
        name_todb = asyncio.create_task(register_name(json))
        return await name_todb
    elif m[0] == 'password':
        m[1] = unquote(m[1])
        m[1] = m[1][:m[1].find('telegramtodelete') - 1]
        json = {'password': m[1], 'id': m[-1]}
        pass_todb = asyncio.create_task(register_password(json))
        return await pass_todb

@app.get("/store")
async def ref_system_post(request: Request):
    return templates.TemplateResponse(name="store.html", request=request)



@app.get("/profile")
async def profile(request: Request):
    return templates.TemplateResponse(name="profile.html", request=request)



@app.post("/profile")
async def ref_system_post(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')
    if m[0] == 'friends':
        profile_data = asyncio.create_task(get_friends(m))
        return await profile_data
    elif m[0]=='profilename':
        profile_data = asyncio.create_task(get_profile(m))
        return await profile_data

@app.post("/riddle")
async def riddle(payload: Any = Body(None)):
    m = payload.decode('utf-8').split('=')
    m[-1]=unquote(m[-1])
    if m[-1] == 'India':
        m = [m[1].split('&')[0],m[-1]]
        return await asyncio.create_task(gift_for_riddle(m))
    return {1:3}
