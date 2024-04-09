# -*- coding: utf-8 -*-
import json
from py.common.sql_log_operation import *
from py.common.globalstuff import transfer_string_from_iso88591_to_utf8
import sys    
sys.stdout.reconfigure(encoding='utf-8')
def newjiang_setting(gs,data):
        print(json.dumps(data, indent=4,ensure_ascii=False))
        p0=transfer_string_from_iso88591_to_utf8(data['p_0'])
        p1=transfer_string_from_iso88591_to_utf8(data['p_1'])
        p2=transfer_string_from_iso88591_to_utf8(data['p_2'])
        p3=transfer_string_from_iso88591_to_utf8(data['p_3'])
        tmp={}
        tmp['jiang-starttime']        =data['time']
        tmp['jiang_this_time_click']  =float(data['circle'])/4
        tmp['player_now']             =[p0,p1,p2,p3]
        tmp['fong_idx']               =0
        tmp['jiang']                  =float(gs.parameters['jiang'])+float(data['circle'])/4
        tmp['liang']                  =0
        tmp['circle']                 =data['circle']
        tmp['start_position']         =data['start_position']
        gs.update_gs_parameters(tmp)
        gs.count_jiang_for_each_player(tmp)
        gs.save_op(data)
        sql_insert_newjiang(gs.log_dbname,gs.parameters)
        return json.dumps(gs.parameters)
