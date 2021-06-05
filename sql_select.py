import json
import mariadb
import sys
import js
import requests
import logging

import jwt

from redis_no import RedisDB

server_token = "123"

headers = {
    "Content-Type": "application/json",
    "Authorization": "key=" + server_token,
}

FILE_SERVER = "http://100.100.100.100"
FILE_REQUEST = f"{FILE_SERVER}/fcm/"

logging.basicConfig(filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s")


def auth(cn, id):
    """
    CLIENT: Authorization
    /client/auth/
    """
    cr = None
    try:
        cr = cn.cursor()
        cr.execute("SELECT"
                   " id,"
                   " content,"
                   " code "
                   "FROM table1 t1"
                   " INNER JOIN table2 t2 ON t1.id = t2.id"
                   " INNER JOIN table3 t3 ON t3.id = t2.num"
                   "WHERE t1.id = %s"
                   "ORDER BY t3.status DESC LIMIT 1", (id, ))
        r = cr.fetchone()
        print("r = ", r)
        return r

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()


def info(cn, id):
    """
    CLIENT: Show information to client
    /client/info/
    """
    msg = []
    list_of_memb = []
    cr = None
    try:
        cr = cn.cursor()
        cr.execute(
            "SELECT table2.id_2 "
            "FROM table1 t1"
            " INNER JOIN table2 t2 ON t1.id = t2.id "
            "WHERE t2.id = %s", (id,)
        )

        rows = cr.fetchall()
        cr.close()

        if rows:
            for r in rows:
                list_of_memb.append(r[0])

        """ ---///--- """

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()

    return msg


def new_info(cn, name, uid, id, phone):
    """
    CLIENT: Insert information about members
    /client/info/upload/
    """
    cr = cn.cursor()
    try:
        """ ---///--- """
        cn.commit()

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()


def insert_news(cn, id, start_date, end_date, content):
    """
    CLIENT: Insert news in web-site
    /client/news/upload/
    """
    cr = None
    try:
        cr = cn.cursor()
        cr.execute(""" ---///--- """)
        cn.commit()

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()


def news(cn):
    """
    CLIENT: Show news to CLIENT3
    /client/news/
    """
    msg = []
    cr = None
    try:
        cr = cn.cursor()
        cr.execute("SELECT"
                   " content,"
                   " start_date,"
                   " end_date "
                   "FROM table1 "
                   "WHERE status = 1"
                   "ORDER BY id DESC")
        rows = cr.fetchall()
        for r in rows:
            msg.append(js.news(r[0], r[1], r[2]))

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        return None

    finally:
        if cr:
            cr.close()

    return msg


def number(cn):
    """
    CLIENT: Show number of processed, submitted, completed project to CLIENT
    /client/number/
    """
    cr = None
    try:
        cr = cn.cursor()
        cr.execute("SELECT COUNT(project_id) "
                   "FROM table1 "
                   "WHERE status IN (\"submitted\")")
        submitted = cr.fetchone()[0]
        cr.execute("SELECT COUNT(project_id) "
                   "FROM table1 "
                   "WHERE status IN (\"processed\")")
        processed = cr.fetchone()[0]
        cr.execute("SELECT COUNT(project_id) "
                   "FROM table1 "
                   "WHERE status IN (\"completed\")")
        completed = cr.fetchone()[0]

        msg = js.info(submitted, processed, completed)

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        return None

    finally:
        if cr:
            cr.close()
    return msg


def request(cn, project_name, last_name, first_name,
                   deadline, status, description, phone, comment,address):
    """
    APPLICATION: Insert NEW APPLICATION from CLIENT into database
    /operator/get_appl/
    """

    try:
        """ ---///--- """

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()

    return {
        "pj_id": id
    }


def s_request(cn, gen_i):
    """
    CLIENT: Show information about project to CLIENT
    /client/request/
    """

    try:
        """ ---///--- """

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()

    return msg


def rate(cn, project_id, rate, comment):
    """
    CLIENT: Update RATE from CLIENT
    /client/get_rate/
    """
    cr = None
    try:
        cr = cn.cursor()
        cr.execute(
            f"UPDATE table1 "
            f"SET rate = {rate}, comment = \"{comment}\" "
            f"WHERE name = %s"
            (project_id,))

        print("row count = ", cr.rowcount)
        if cr.rowcount != 0:
            cn.commit()
        else:
            raise Exception("Ошибка. Обновления не сохранились. Попробуйте позже.")

    except Exception as e:
        err = sys.exc_info()
        print("ERROR", err, err[-1].tb_lineno)
        logging.exception(e)
        raise

    finally:
        if cr:
            cr.close()


def dscn_db(cn):
    """
    Disconnect database
    """
    cn.close()


def cn_db():
    """
    Connect database MariaDB
    """
    try:
        cn = mariadb.connect(

            user="aktumar",
            password="asdqwe",
            host="100.100.100.100",
            port=1010,
            database="database1"
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    print("Connected to mariadb successfully")
    return cn
