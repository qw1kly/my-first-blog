import asyncio
import aiomysql


async def check_pass(m):
    connect = await aiomysql.connect(host='localhost', port=3306, user='root', password='azik959595', db='game')
    sel = 'SELECT * FROM password'
    async with connect.cursor() as cur:
        await cur.execute(sel)
        auths = await cur.fetchall()
        for i in auths:
            if m[0] == i[0] and m[1]==i[1]:
                connect.close()
                return True
        connect.close()
        return False