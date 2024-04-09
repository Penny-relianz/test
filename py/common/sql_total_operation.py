# -*- coding: utf-8 -*-
'''
# -*- coding: utf-8 -*-
'''
import time
import sqlite3
import os
import sys
import traceback
import json

def get_latest_log_table(dbname):
        conn = sqlite3.connect(dbname)
        sqlcmd = "SELECT name FROM sqlite_master WHERE type='table';"
        print (sqlcmd)
        cursor=conn.execute(sqlcmd)
        #show all tables.
        tables = [
                v[0] for v in cursor.fetchall()
                if v[0] != "sqlite_sequence"
        ]
        if tables:
                latesttable=tables[-1]
        else:
                conn.close()
                return '{"status":999}'
        conn.commit()
        conn.close()
        return latesttable
def get_content_from_table(dbname,tbname):
        conn = sqlite3.connect(dbname)
        sqlcmd = 'select * from %s'%(tbname)
        cursor = conn.execute(sqlcmd)
        data=cursor.fetchall()
        conn.close()
        return data

        
def sql_insert(parameters,tbtype,dbname):
        conn = sqlite3.connect(dbname)
        #conn.enable_load_extension(True)
        #conn.load_extension("json1.dll")
        #sqlcmd  = 'INSERT INTO %s VALUES %s;'%(tbname,data)
        if tbtype=="log":
                sqlcmd  = "insert into LOG_{t}(parameters) values('{json_op}');".format(t=parameters['log-starttime'],json_op=json.dumps(parameters))
        elif tbtype=="record":
                sqlcmd  = "insert into LOG_{t}(parameters) values('{json_op}');".format(t=parameters['log-starttime'],json_op=json.dumps(parameters))
         
        #print sqlcmd
        conn.execute(sqlcmd) 
        conn.commit()
        conn.close()
def sql_createtable(parameters,tbtype,dbname):
        conn = sqlite3.connect(dbname)
        print ("Opened database successfully");
        
        if tbtype =="log":
                sqlcmd='''
                CREATE TABLE  if not exists LOG_{t}
                (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
                parameters blob(1024)NOT NULL
                );
                '''.format(t=parameters['log-starttime'])
        conn.execute(sqlcmd)
        conn.close()
        print ("%s Table created successfully"%(tbtype));
        
        return
def sql_insert_newjiang(dbname,parameters):
        conn = sqlite3.connect(dbname)
        print(json.dumps(parameters, indent=4))
        parameters['op']['action']="new%d"%parameters['jiang']
        sqlcmd  = "insert into LOG_{t}(parameters) values('{json_op}');".format(t=parameters['log-starttime'],json_op=json.dumps(parameters))
        conn.execute(sqlcmd)   
        conn.commit()
        conn.close()        
        print("new%d insert successful"%parameters['jiang'])
        return
        
#status 999     error
#       998     empty table
def sql_get_last_gs(dbname):
        latesttable=get_latest_log_table(dbname)
        if latesttable=='{"status":999}':
                print("get lates table fail...")
                return '{"status":999}'
        conn = sqlite3.connect(dbname) 
        print (latesttable)
        str_data=get_content_from_table(dbname,latesttable)
        print (type(str_data))
        if str_data:
                try:
                        parameters=json.loads(str_data[-1][1])
                except:
                        conn.close()
                        print("json loads fail...")
                        return '{"status":999}'
                conn.close()
                return parameters
        else:
                return '{"status":998}'
def sql_get_log(dbname):
        
        latesttable=get_latest_log_table(dbname)
        if latesttable=='{"status":999}':
                return '{"status":999}'
        logs=[]
        conn = sqlite3.connect(dbname)        
        data=get_content_from_table(dbname,latesttable)
        for one_gs in data:
                try:
                        one_gs_dict=json.loads(one_gs[1])
                        logs.append(one_gs_dict["op"])
                except Exception as e:
                        conn.close()
                        return e
        
        
        conn.close()
        return logs
        

def sql_clear_last(dbname):
        latesttable=get_latest_log_table(dbname)
        if latesttable=='{"status":999}':
                return '{"status":999}'
                
        conn = sqlite3.connect(dbname)
        sqlcmd="delete from {0} WHERE ID = (SELECT MAX(ID) FROM {0});".format(latesttable)   
        print (sqlcmd)
        conn.execute(sqlcmd)
        conn.commit()
        #data=cursor.fetchall()
        #print (str(data))
        conn.close()
        
        
        
def first_create_statistic_table(dbname):
        pass
def insert_new_player(dbname):
        pass
def update_info(action,dbname):
        pass
        
        
        
        
        
        
        
        
        
        
        
        