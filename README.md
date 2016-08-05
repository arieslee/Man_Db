# Man_Db
###一个基于[pymysql](https://github.com/PyMySQL/PyMySQL)模块的mysql操作类
####DEMO
```python
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
    sql = 'SELECT * FROM '+db.table('articles')+' WHERE id=%s LIMIT 0,1'
    if db.query(sql ,(1,)):
        row = db.fetch_one()
        print row
    # SELECT many
    sql = 'SELECT * FROM '+db.table('articles')+' WHERE id>%s LIMIT 0,10'
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
        'title':'This is a test for update'
    }
    res = db.update('articles' ,updates ,'id=10')
    if res is not False:
        db.commit()
    # DELETE
    res = db.delete('articles' ,'id=%s',(2,))
    if res is not False:
        db.commit()
```
