#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/5 15:58
# @Author  : Aries (i@iw3c.com)
# @Site    : http://iw3c.com
# @File    : demo.py.py
# @Software: PyCharm

from Man_Db import *
import time
if __name__ == '__main__':
    db = Man_Db({
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'name': 'man_db_read',
            'charset': 'utf8',
            'prefix': 'man_'
        })
    # SELECT one
    sql = 'SELECT * FROM '+db.table('articles')+' LIMIT 0,1'
    if db.query(sql):
        row = db.fetch_one()
        print row
    # SELECT many
    '''sql = 'SELECT * FROM '+db.table('articles')+' WHERE id>%s LIMIT 0,10'
    if db.query(sql,(1,)):
        rows = db.fetch_all()
        for r in rows:
            print r
    # INSERT
    datas = {
        'content':'This is content',
        'status':0,
        'created':int(time.time()),
        'title':'This is title'
    }
    id = db.insert('articles' ,datas)
    if id > 0 :
        db.commit()
    # UPDATE
    updates = {
        'title':'This is a test for update',
        'views':{'+',1}
    }
    res = db.update('articles' ,updates ,'id=10')
    if res is not False:
        db.commit()
    # OR UPDATE
    res = db.update('articles', updates, 'id=:%s',(10,))
    if res is not False:
        db.commit()
    # DELETE
    res = db.delete('articles' ,'id=%s',(2,))
    if res is not False:
        db.commit()'''
