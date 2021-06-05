import jwt
import sys
import json
import logging
import requests

from fastapi.responses import ORJSONResponse
from fastapi import FastAPI, status
from datetime import date

import sql_select as sql
import js_models as js

logging.basicConfig(filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")

key = "s5be63t1b3sd5rts54rg1fvds1v2sdv"

FILE_SERVER = "http://100.100.100.100"
FILE_REQUEST = f"{FILE_SERVER}/auth/"

app = FastAPI()


@app.post("/client/auth/", response_class=ORJSONResponse)
async def auth(msg: js.auth):
    """
    CLIENT: Authorization

    request:
        phone - "77017777777"
        jwt

    response:
        key
        id - organization id
        name - organization name
    """
    cn = None
    try:
        m = RedisDB()
        obj = m.read(msg.phone)
        jwt.decode(msg.jwt, obj["sk"], algorithms=["HS256"])

    except jwt.exceptions.InvalidSignatureError or jwt.exceptions.ExpiredSignatureError:
        print("ERROR jwt")
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Ошибка авторизации"
        }

    try:
        cn = sql.cn_db()
        rq = sql.auth(cn, obj["id"])
    except:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Произошла внутренняя ошибка сервера. Попробуйте позже"
        }
    finally:
        if cn:
            sql.dscn_db(cn)

    if rq:
        return {
            "status": status.HTTP_200_OK,
            "dat": {
                "key": key,
                "id": rq[0],
                "name": rq[1],
            }

        }
    else:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Ваш номер не был зарегистрирован"
        }


@app.post("/client/info/", response_class=ORJSONResponse)
async def info(msg: js.info):
    """
    CLIENT: Show information to client

    request:
        id
        key

    response:
        id
        name
        phone
        team - [names]
    """
    cn = None
    try:
        cn = sql.cn_db()
        rq = sql.info(cn, msg.id)
    except:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Произошла внутренняя ошибка сервера. Попробуйте позже",
        }
    else:
        return {
            "status": status.HTTP_200_OK,
            "dat": rq,
            "key": key
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.post("/client/info/upload/", response_class=ORJSONResponse)
async def new_info(msg: js.new_info):
    """
    CLIENT: Insert information about members

    request:
        name - Name of new member
        id - id of new member
        phone - 77017777777
        key
    """
    cn = None
    uid = None

    js_rq = {
        "name": msg.name,
        "id": msg.id,
        "phone": msg.phone
    }

    try:
        r = requests.post(FILE_REQUEST, data=json.dumps(js_rq))
        rd = json.loads(r.content)

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Не удалось сохранить новый сектор. Попробуйте позже",
        }

    try:
        cn = sql.cn_db()
        sql.new_info(cn, msg.name, uid, msg.id, msg.phone)

    except:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Не удалось сохранить новый сектор. Попробуйте позже",
        }
    else:
        return {
            "status": status.HTTP_200_OK,
            "key": key
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.post("/client/news/upload/", response_class=ORJSONResponse)
async def news(msg: js.news):
    """
    CLIENT: Insert news in web-site

    request:
        id - id of CLIENT
        start_date - start date
        end_date - end date
        content - content of news in russian
    """
    cn = None
    try:
        cn = sql.cn_db()
        sql.insert_news(
            cn, msg.id,
            msg.start_date,
            msg.end_date,
            msg.content
        )
    except:
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "error": "Не удалось создать оповещение. Попробуйте позже",
        }
    else:
        return {
            "status": status.HTTP_200_OK,
            "key": key
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.get("/client/news/", response_class=ORJSONResponse)
async def news():
    """
    CLIENT: Show news to CLIENT

    response:
        content - content of news
        start_date - start date
        end_date - end date
    """
    cn = sql.cn_db()
    rq = sql.news(cn)
    sql.dscn_db(cn)
    if rq is None:
        return {
            "status": status.HTTP_400_BAD_REQUEST
        }
    else:
        return {
            "status": status.HTTP_200_OK,
            "dat": rq
        }


@app.get("/client/number/")
async def number():
    """
    CLIENT: Show number of processed, submitted, completed project to CLIENT

    response:
        submitted
        processed
        completed
    """
    cn = None
    try:
        cn = sql.cn_db()
        rq = sql.number(cn)
    except:
        return {"status": status.HTTP_400_BAD_REQUEST}
    else:
        return {
            "status": status.HTTP_200_OK,
            "dat": rq
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.post("/client/request/upload/")
async def request(msg: js.request):
    """
    CLIENT: Insert information about project

    request:
        project_name
        last_name
        first_name
        deadline, for example "2020-08-20"
        status
        description
        phone
        comment
        address

    response:
        pj_id
    """
    cn = None
    try:
        cn = sql.cn_db()
        rq = sql.request(
            cn,
            msg.project_name,
            msg.last_name,
            msg.first_name,
            msg.deadline,
            msg.status,
            msg.description,
            msg.phone,
            msg.comment,
            msg.address
        )
    except:
        return {"status": status.HTTP_400_BAD_REQUEST}
    else:
        return {
            "status": status.HTTP_200_OK,
            "dat": rq
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.post("/client/request/", response_class=ORJSONResponse)
async def request(msg: js.request):
    """
    CLIENT: Show information about project to CLIENT

    request:
        id
        key

    response:
        id
        name
        member_id
        deadline
        status
        created_date
        description
        comment
        address
    """
    cn = None
    try:
        cn = sql.cn_db()
        rq = sql.s_request(cn, msg.id)
    except:
        return {"status": status.HTTP_400_BAD_REQUEST,
                "error": "Произошла внутренняя ошибка сервера. Попробуйте позже",
                }
    else:
        return {
            "status": status.HTTP_200_OK,
            "dat": rq,
            "key": key
        }
    finally:
        if cn:
            sql.dscn_db(cn)


@app.post("/client/get_rate/")
async def rate(msg: js.rate):
    """
    CLIENT: Update RATE from CLIENT

    request:
        project_id
        comment
        rate
    """
    cn = None
    try:
        cn = sql.cn_db()
        sql.rate(cn, msg.project_id, msg.rate, msg.comment)
    except:
        return {"status": status.HTTP_400_BAD_REQUEST}
    else:
        return {"status": status.HTTP_200_OK}
    finally:
        if cn:
            sql.dscn_db(cn)
