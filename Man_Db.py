#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/8/5 10:16
# @Author  : Aries (i@iw3c.com)
# @Site    : http://iw3c.com
# @File    : Man_Db.py
# @Software: PyCharm
# @Need pymysql lib (Install : pip install PyMySQL)
import pymysql.cursors
class Man_Db():
    __connect = None  # 数据库链接
    __cursor = None   # 数据库游标
    __last_query = None
    __config = {
        'host': 'localhost',
        'user': '',
        'password': '',
        'name': '',
        'charset': 'utf8',
        'prefix':'db_'
    }    # 数据库配置信息

    def __init__(self, config):
        self.__config = config

    def connect(self):
        '''
        数据库连接
        :return:
        '''
        try:
            self.__connect = pymysql.connect(host=self.__config['host'],
                                            user=self.__config['user'],
                                            password=self.__config['password'],
                                            db=self.__config['name'],
                                            charset=self.__config['charset'],
                                            cursorclass=pymysql.cursors.DictCursor)
            self.__cursor = self.__connect.cursor()
            return True
        except pymysql.Error as e:
            print("Mysql Connect Error: %s" % (e,))
            exit()
            return False

    def connected(self):
        '''
        数据库是否连接
        :return:
        '''
        return self.__connect is not None

    def table(self, td, as_td=None):
        table = '`' + self.__config['name'] + '`.' + '`' + self.__config['prefix'] + td + '`'
        if as_td is not None:
            table = table + ' AS ' + as_td
        return table
    @property
    def cursor(self):
        '''
        获取当前指针
        :return:
        '''
        return self.__cursor
    @property
    def config(self):
        '''
        获取当前的配置信息
        :return:
        '''
        return self.__config
    @config.setter
    def config(self, value):
        self.__config = value
    @property
    def last_query(self):
        '''
        获取最后一次执行的SQL
        :return:
        '''
        return self.__last_query

    def query(self, sql, params=None):
        '''
        执行SELECT语句
        :param sql:
        :param params:
        :return:
        '''
        if self.connected() is False:
            self.connect()
        self.__last_query = sql
        try:
            if params is not None:
                result = self.__cursor.execute(sql, params)
            else:
                result = self.__cursor.execute(sql)
        except pymysql.Error as e:
            result = False
            print("Mysql Error: %s\nOriginal SQL:%s" % (e, sql))
        return result

    def insert(self, table, datas):
        '''
        执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
        :param table:
        :param datas:
        :return:
        '''
        columns = datas.keys()
        _prefix = "".join(['INSERT INTO ', self.table(table)])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [datas[key] for key in columns]
        self.__last_query = _sql
        if self.connected() is False:
            self.connect()
        try:
            self.__cursor.execute(_sql, tuple(_params))
            return self.insert_id()
        except pymysql.Error as e:
            print("Mysql Error: %s" % (e,))
        return False

    def insert_id(self):
        '''
        最后一次插入后得到的ID
        :return:
        '''
        return self.__cursor.lastrowid

    def update(self, table, datas, where, params=None):
        '''
        更新数据
        :param table:
        :param datas:
        :param where:
        :param params:
        :return:
        '''
        _fields = []
        _values = []
        _prefix = "".join(['UPDATE ', self.table(table), ' SET '])
        for key in datas.keys():
            _fields.append('`'+key+'`=%s')
        for val in datas.values():
            if isinstance(val, dict) is True:
                _values.append(str(val.keys()[0]) + str(val.values()[0]))
            else:
                _values.append(val)
        _sql = "".join([_prefix, ','.join(str(v) for v in _fields), " WHERE ", where])
        if params is not None and isinstance(params, tuple):
            binds = tuple(_values) + params
        else:
            binds = tuple(_values)

        if self.query(_sql, binds) is not False:
            return self.get_row_count()
        return False

    def delete(self, table, where, params=None):
        '''
        删除操作
        :param table:
        :param where:
        :param params:
        :return:
        '''
        _prefix = "".join(['DELETE FROM  ', self.table(table), ' WHERE '])
        _sql = "".join([_prefix, where])
        if self.query(_sql, params) is not False:
            return self.get_row_count()
        return False

    def fetch_all(self):
        '''
        返回结果列表
        :return:
        '''
        return self.__cursor.fetchall()

    def fetch_one(self):
        '''
        返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
        :return:
        '''
        return self.__cursor.fetchone()

    def close(self):
        '''
        关闭数据库连接
        :return:
        '''
        try:
            self.__connect.close()
            self.__cursor.close()
        except:
            pass

    def __del__(self):
        self.close()

    def get_row_count(self):
        '''
        获取结果行数
        :return:
        '''
        return self.__cursor.rowcount

    def commit(self):
        '''
        数据库commit操作
        :return:
        '''
        if self.connected():
            try:
                self.__connect.commit()
            except :
                pass

    def rollback(self):
        '''
        数据库回滚操作
        :return:
        '''
        if self.connected():
            try:
                self.__connect.rollback()
            except:
                pass