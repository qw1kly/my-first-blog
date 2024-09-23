import asyncio
import aiomysql
import aiofiles
import os

async def game_ch(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    multiaccess = f"SELECT * FROM users WHERE tele_id='{m[1]}'"
    ins = f"INSERT INTO games VALUES(id, '{m[-1]}')"
    sel = f'SELECT * FROM games WHERE id=(SELECT MAX(id) FROM games);'
    sel_users = f'SELECT * FROM users WHERE tele_id="{m[1]}"'
    async with connect.cursor() as cur:
        await cur.execute(multiaccess)
        actbal = await cur.fetchone()
        if actbal[-2] == "0":
            connect.close()
            return {"1": 0}
        await cur.execute(ins)
        await cur.execute(sel_users)
        balance = await cur.fetchone()
        upd = f"UPDATE users SET balance = {int(balance[1]) - 1} WHERE tele_id ='{m[1]}'"
        await cur.execute(sel)
        last_id = await cur.fetchone()
        if last_id[0] % 10 == 0:
            upd = f"UPDATE users SET balance = {int(balance[1]) + 199} WHERE tele_id ='{m[1]}'"
            await cur.execute(upd)
            win_us = f'SELECT * FROM winners WHERE tel_id="{m[1]}"'
            await cur.execute(win_us)
            win = await cur.fetchone()
            update_win = f"UPDATE winners SET access = {int(win[1]) + 200} WHERE tel_id ='{m[1]}'"
            await cur.execute(update_win)
            await connect.commit()
            connect.close()
            return {'1': 1}
        await cur.execute(upd)
        await connect.commit()
    connect.close()
    return {'1': 0}


async def auth(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = f"SELECT * FROM users"
    async with connect.cursor() as cur:
        await cur.execute(sel)
        usr = await cur.fetchall()
        for i in usr:
            if m[1] in i:
                connect.close()
                return {'1': [int(i[1]), int(i[2])]}
        await connect.commit()
    connect.close()

    return {'1': [0,0]}


async def register(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = 'SELECT * FROM registration'
    async with connect.cursor() as cur:
        await cur.execute(sel)
        all = await cur.fetchall()
        for i in all:
            if m[1] in i:
                connect.close()
                return {1:1}
    connect.close()
    return {1:0}


async def rat_auth(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = f"SELECT * FROM users"
    sel_top = f"SELECT * FROM winners"
    async with connect.cursor() as cur:
        await cur.execute(sel)
        usr = await cur.fetchall()
        await cur.execute(sel_top)
        winners = list(map(lambda y: y[0], sorted(await cur.fetchall(), key=lambda x: x[1], reverse=True)[:5]))
        for i in usr:
            if m[1] in i and m[1] in winners:
                await connect.commit()

                connect.close()
                return {'1': int(i[1]), '2': 1}
            elif m[1] in i and m[1] not in winners:
                await connect.commit()

                connect.close()
                return {'1': int(i[1]), '2': 0}
    connect.close()
    return {'1':0, '2': 0}


async def one_win(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    select = 'SELECT * FROM winners'
    select2 = 'SELECT * FROM registration'
    async with connect.cursor() as cur:
        await cur.execute(select2)
        usr = await cur.fetchall()
        flag = False
        for i in usr:
            if m[1] in i:
                flag = True
                break
        if flag == False:
            connect.close()
            return {1:0}
        await cur.execute(select)
        winners = await cur.fetchall()
        winners = list(map(lambda y: list(y), winners))
        winners.sort(key=lambda x: x[1], reverse=True)
        for j in range(len(winners)):
            if i[0] in winners[j]:
                connect.close()
                return {1: j+1, 2:i[1], 3:winners[j][1]}

    connect.close()
    return {1:0}


async def rat_win(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel1 = "SELECT * FROM registration"
    sel2 = "SELECT * FROM winners"
    async with connect.cursor() as cur:
        await cur.execute(sel1)
        users_name = await cur.fetchall()
        await cur.execute(sel2)
        winners = await cur.fetchall()
        winnerscopy = list(winners).copy()
        winners = list(map(lambda y: list(y), winners))
        winners.sort(key=lambda x: x[1], reverse=True)
        winners = winners[:5]
        print(winnerscopy[:5], winners)
        if winnerscopy[:5]==winners:
            winners.sort(key=lambda x: x[0])
        access_with_winners = [0,0,0,0,0]
        index = 0
        for i in winners:
            for j in users_name:
                if i[0] in j:
                    access_with_winners[index]=j[1]
                    index+=1
    connect.close()
    return {0:access_with_winners[0],1:access_with_winners[1],2:access_with_winners[2],3:access_with_winners[3],4:access_with_winners[4],5:winners[0][1],6:winners[1][1],7:winners[2][1],8:winners[3][1],9:winners[4][1]}


async def referation_system(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    ins = 'INSERT INTO referals (ref_id, child_id) values (%s, %s)'
    sel = 'SELECT * FROM referals'
    sel_point = 'SELECT * FROM points'
    access = 'SELECT * FROM registration'
    insi = 'INSERT INTO pointersid (child, referal, points) values (%s, %s, %s)'
    async with connect.cursor() as cur:
        index_list = m[1][1].rfind("%2F")
        m_ref = [m[0][1], m[1][1][index_list + 3:]]
        vals = tuple(m_ref)

        await cur.execute(sel)
        refers = await cur.fetchall()
        for i in refers:
            if m_ref[0] == i[0] or m_ref[0] == m_ref[1]:
                connect.close()
                return False
        valuevi = (m_ref[0], m_ref[1], 0)
        await cur.execute(insi, valuevi)
        await cur.execute(sel_point)
        pointers = await cur.fetchall()
        upd = ''
        for i in pointers:
            if m_ref[1] in i:
                upd = True
                break

        if upd == '':
            ins_2 = 'INSERT INTO points (id_of, points) values (%s, %s)'
            vals2 = (m_ref[1], 0)
            await cur.execute(ins_2, vals2)
        await cur.execute(ins, vals)
        await connect.commit()
    connect.close()


async def register_name(json):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    ins = "INSERT INTO registration (telegram, name, photo) values (%s, %s, %s)"
    inser = "INSERT INTO users (tele_id, balance, usdt) values (%s, %s, %s)"
    insert = "INSERT INTO winners (tel_id, access) values(%s, %s)"
    sel = "SELECT * FROM registration"
    async with connect.cursor() as cur:
        await cur.execute(sel)
        usr_fals = await cur.fetchall()
        for i in usr_fals:
            if json['id'] in i:
                connect.close()
                return {1:2}
            if json['nickname'] in i:
                connect.close()
                return {1:2}
    for i in json['nickname']:
        if i not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890':

            connect.close()
            return {1:0}
    if 5<=len(json['nickname'])<=20 and json['nickname'][0] not in '0123456789':
        val = (json['id'], json['nickname'], f'avatars/{json["id"]}.png')
        val_2 = (json['id'], 0, 0)
        val_3 = (json['id'], 0)
        async with connect.cursor() as cur:
            await cur.execute(ins, val)
            await cur.execute(inser, val_2)
            await cur.execute(insert, val_3)
            await connect.commit()
        connect.close()
        return {1:1}

    connect.close()
    return {1:0}


async def get_nickname(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = 'SELECT * FROM registration'
    async with connect.cursor() as cur:
        await cur.execute(sel)
        names = await cur.fetchall()
        for i in names:
            if m[1] in i:
                connect.close()
                return {1:i[1]}
    connect.close()
    return {1:'notfound'}


async def get_profile(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel_1 = 'SELECT * FROM users'
    sel_2 = 'SELECT * FROM registration'
    async with connect.cursor() as cur:
        await cur.execute(sel_1)
        users_bal = await cur.fetchall()
        await cur.execute(sel_2)
        users_name = await cur.fetchall()
        bal = []
        for i in users_bal:
            if m[1] in i:
                bal = [i[1],i[2]]
                break
        for i in users_name:
            if m[1] in i:
                connect.close()
                return {1:i[1],2:bal[0],3:bal[1]}



async def get_friends(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel1 = 'SELECT * FROM referals'
    get_name = "SELECT * FROM registration"
    get_act = "SELECT * FROM pointersid"
    async with connect.cursor() as cur:
        friends = []
        await cur.execute(sel1)
        take_friends = await cur.fetchall()
        await cur.execute(get_act)
        take_points = await cur.fetchall()
        await cur.execute(get_name)
        take_name = await cur.fetchall()
        names = []
        for i in take_friends:
            if m[1]==i[1]:
                friends.append(i[0])
        for i in take_name:
            if i[0] in friends:
                ind = friends.index(i[0])
                friends[ind]=[i[1], i[0]]
        for i in take_points:
            if m[1] == i[1]:
                child_id = i[0]
                for j in range(len(friends)):
                    if child_id in friends[j]:
                        friends[j].append(i[2]+1)
        dicta = {}
        count=0
        for i in range(len(friends)):
            dicta[count] = friends[0]
            dicta[count+1] = friends[1]
            dicta[count+2] = friends[2]
            dicta[count+3]= 'END'
            count+=4
        connect.close()
        return dicta


async def auth_password(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    select = "SELECT * FROM password"
    select2 = "SELECT * FROM winners"
    select3 = "SELECT * FROM riddles"
    async with connect.cursor() as cur:
        await cur.execute(select3)
        riddlers = await cur.fetchall()
        await cur.execute(select2)
        winners = await cur.fetchall()
        winners = list(map(lambda y: list(y), winners))
        winners.sort(key=lambda x: x[1], reverse=True)
        winners = winners[:5]
        await cur.execute(select)
        users = await cur.fetchall()
        for i in users:
            if m[0] == i[0] and m[1] == i[1]:
                for j in riddlers:
                    if m[0] == j[0]:
                        connect.close()
                        return {1:1}
        for i in users:
            if m[0]==i[0] and m[1]==i[1]:
                for j in winners:
                    if m[0] == j[0]:
                        connect.close()
                        return {1:1}
                connect.close()
                return {1:0}
        connect.close()
        return {1:0}


async def register_password(json):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    select = "SELECT * FROM password"
    ins = "INSERT INTO password (telegram, pass) values (%s, %s)"
    async with connect.cursor() as cur:
        await cur.execute(select)
        passes = await cur.fetchall()
        for i in passes:
            if json['id'] in i:
                connect.close()
                return {1:0}
        if 8<=len(json['password'])<=15:
            await cur.execute(ins, (json['id'], json['password']))
            await connect.commit()
            connect.close()
            return {1:1}
        connect.close()
        return {1:2}

async def auth_check_password(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    select_ = 'SELECT * FROM password'
    async with connect.cursor() as cur:
        await cur.execute(select_)
        usrs = await cur.fetchall()
        for i in usrs:
            if i[0]==m[0] and i[1]==m[1]:
                connect.close()
                return {1:1}
            elif i[0]==m[0] and i[1]!=m[1]:
                connect.close()
                return {1:0}
        connect.close()
        return {1:2}

async def gift_for_riddle(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = "SELECT * FROM users"
    sel_2 = "SELECT * FROM riddles"
    ins = "INSERT INTO riddles (telegram_unique_id, riddle) values (%s, %s)"
    async with connect.cursor() as cur:
        await cur.execute(sel_2)
        riddles = await cur.fetchall()
        for i in riddles:
            if m[-1] in i:
                connect.close()
                return {1:0}
        await cur.execute(sel)
        user_balance = await cur.fetchall()
        for i in user_balance:
            if m[0] == i[0]:
                ins1 = f'UPDATE users SET balance = {int(i[1]) + 1000} WHERE tele_id = {m[0]}'
                await cur.execute(ins1)
                val = (m[0],m[-1])
                await cur.execute(ins, val)
                await connect.commit()
                connect.close()
                return {1:1}
        return {1:2}