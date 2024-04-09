
import json
import os

import sys    
import sqlite3

#sys.stdout.reconfigure(encoding='utf-8')
import sqlite3
from py.common.sql_log_operation import *
from datetime import datetime
from datetime import date
def transfer_string_from_iso88591_to_utf8(s):
        try:
                s=s.encode('iso-8859-1').decode('utf-8')
        except:
                print('utf8')
        return s
                
def get_now_time_str():
                print ("create a new log-time")
                now = datetime.now()
                today= date.today()
                current_time = now.strftime("%H%M")
                day = today.strftime("%Y%m%d")
                str_date=day+"_"+current_time
                return str_date
class globalstuff():
        def __init__(self):
                self.log_dbname="soga_log.db"
                self.statistic_dbname="soga.db"
                self.get_latest_gs()
        
        def create_new_gs(self,str_date):
                self.parameters={
                        "op":"",
                        "log-starttime":str_date,
                        "jiang-starttime":"",
                        "fong_idx":0,     #0-15 東風東~北風北
                        "jiang":0,        #打到第幾將
                        "liang":0,        #目前連莊數
                        "player_now":[],  #場上四位玩家
                        "player_today_record":{},#今天出戰過的玩家
                        "circle":0.0,
                        "start_position":0,
                        "de":3,           #底點數
                        "tai":1           #台點數
                }  
        def get_latest_gs(self):
                if os.path.isfile(self.log_dbname):
                        print("%s exist"%self.log_dbname)
                        self.parameters=sql_get_last_gs(self.log_dbname)
                        if self.parameters=='{"status":999}':
                                #get data from sql fail
                                print ("error for some reason")
                                t=get_now_time_str()
                                self.create_new_gs(t)
                                self.create_new_log_table_in_sql()
                                return 0
                        if self.parameters=='{"status":998}': 
                                print ("empty table exist...init gs only")
                                self.get_latest_log_table_time_from_sql()
                        return 1
                else:
                        print ("DB do not exist...")
                        t=get_now_time_str()
                        self.create_new_gs(t)
                        self.create_new_log_table_in_sql()
                        return 0
                pass
        
        def get_latest_log_table_time_from_sql(self):
                logname=get_latest_log_table(self.log_dbname)
                time_str=logname[4:]
                self.create_new_gs(time_str)
        def update_gs_parameters(self,data):
                for key, value in data.items():
                        #print(key+"="+str(value))
                        if type(value)==list:
                                self.parameters[key]=[]
                                for idx,item in enumerate(value):
                                        self.parameters[key].append(item)
                        if type(value)==dict:
                                for value_key, value_value in value.items():
                                        pass
                        else:
                                #print("self.parameters[key]=value, key=%s,value=%s"%(key,str(value)))
                                self.parameters[key]=value     
                
        def count_jiang_for_each_player(self,data):
                for playername in data['player_now']:
                        if playername in self.parameters['player_today_record']:
                                print (playername+ "exist")
                                self.parameters['player_today_record'][playername]['playjiang']+=data['jiang_this_time_click'];
                        else:
                                print ("append new player :"+playername )
                                self.parameters['player_today_record'][playername]={};
                                self.parameters['player_today_record'][playername]['point']=0;
                                self.parameters['player_today_record'][playername]['zhmo']=0;
                                self.parameters['player_today_record'][playername]['hu']=0;
                                self.parameters['player_today_record'][playername]['gun']=0;
                                self.parameters['player_today_record'][playername]['playjiang']=1;
                                self.parameters['player_today_record'][playername]['bai_mo']=0;
                                self.parameters['player_today_record'][playername]['nothing']=0;
                                #Current_player_on_the_groundcnt++;
                
        def get_banker_name(self):
                self.parameters['banker_name']=self.parameters['player_now'][self.parameters['fong_idx']%4]
        def create_new_log_table_in_sql(self):
                sql_createtable(self.parameters,"log",self.log_dbname)
        def save_action_to_sql(self):
                sql_insert(self.parameters,"log",self.log_dbname)
        def save_op(self,data):
                self.parameters["op"]=data
                self.parameters['op']['point']={}
                for player in self.parameters['player_now']:
                        self.parameters['op']['point'][player]=0
                self.get_banker_name()        
               
                