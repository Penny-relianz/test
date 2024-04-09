import json
import time
from py.common.globalstuff import get_now_time_str
from py.common.globalstuff import transfer_string_from_iso88591_to_utf8
import sqlite3
def do_statistic_db_update(gs_obj):
        print("Update statistic sqlite")
        #print(json.dumps(gs_obj, indent=4))
        player_record=gs_obj['player_today_record']

        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS soga_record (
                                        ID INTEGER PRIMARY KEY   AUTOINCREMENT,
                                        name text NOT NULL UNIQUE,
                                        POINT INT  NOT NULL,
                                        自摸 INT  NOT NULL,
                                        放槍 INT  NOT NULL,
                                        胡牌 INT  NOT NULL,
                                        被摸 INT  NOT NULL,
                                        將數 INT  NOT NULL
                                    ); """


        conn=sqlite3.connect("soga_record.db")
        conn.execute(sql_create_projects_table)
        conn.commit()
        for p,info in player_record.items():
                p=transfer_string_from_iso88591_to_utf8(p)
                #sqlcmd="select * from soga_record where name=\"%s\""%p
                #crsr = conn.cursor()
                #crsr.execute(sqlcmd)

                sqlcmd="INSERT OR IGNORE INTO soga_record (name,POINT,自摸,放槍,胡牌,被摸,將數) VALUES(\"%s\",%d,%d,%d,%d,%d,%d);"%(p,0,0,0,0,0,0)
                #print (sqlcmd)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET POINT=POINT+%d where name=\"%s\";"%(info['point'],p)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET 自摸=自摸+%d where name=\"%s\";"%(info['zhmo'],p)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET 放槍=放槍+%d where name=\"%s\";"%(info['gun'],p)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET 胡牌=胡牌+%d where name=\"%s\";"%(info['hu'],p)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET 被摸=被摸+%d where name=\"%s\";"%(info['bai_mo'],p)
                conn.execute(sqlcmd)
                conn.commit()
                sqlcmd="UPDATE soga_record SET 將數=將數+%d where name=\"%s\";"%(info['playjiang'],p)
                conn.execute(sqlcmd)
                conn.commit()
        conn.close()
        get_info_from_statistic_db()
def get_info_from_statistic_db():
        try:
                conn=sqlite3.connect("soga_record.db")
                crsr = conn.cursor()
                crsr.execute("select * from soga_record  order by point DESC  ")
                result = crsr.fetchall()
                print(result)
                conn.close()
        except:
                result=[]
        return result