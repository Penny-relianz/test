
import json
import sys    
#sys.stdout.reconfigure(encoding='utf-8')

from py.common.globalstuff import transfer_string_from_iso88591_to_utf8
def do_action(gs,data):
        print (data)
        ###################################
        data['winner']=transfer_string_from_iso88591_to_utf8(data['winner'])
        data['loser']=transfer_string_from_iso88591_to_utf8(data['loser'])
        ####################################

        gs.save_op(data)
        if "btnHU" in data['action']:
                HU(gs,data)
        elif "btnZHMO" in data['action']:
                ZHMO(gs,data)
        elif "btnZAHU" in data['action']:  
                # winner =詐胡者  loser=不指定
                data['tai']=5
                ZAHU(gs,data)
        elif "btnPONG" in data['action']:
                #喊碰不碰
                PONG_NO_PONG(gs,data)
        elif "btnTHREEPONG" in data['action']:
                THREE_SIANG(gs)
        if not "btnPONG" in data['action']:
                liangzhung(gs)     
        print(json.dumps(gs.parameters, indent=4))
        gs.save_action_to_sql()
        return json.dumps(gs.parameters)
        
def calculate_point(gs,tai):
        point=int(tai)*gs.parameters['tai']+gs.parameters['de']
        return point        
def pay(gs,win,lose,point):
        gs.parameters['player_today_record'][win]['point']+=point
        gs.parameters['player_today_record'][lose]['point']-=point
        gs.parameters['op']['point'][win]+=point
        gs.parameters['op']['point'][lose]-=point
def HU(gs,data):
        point=calculate_point(gs,gs.parameters['op']['tai'])
        for player in gs.parameters['player_now']:
                if data['winner'] == player:
                        gs.parameters['player_today_record'][player]['hu']+=1
                elif data['loser'] == player :
                        gs.parameters['player_today_record'][player]['gun']+=1
                else:
                        gs.parameters['player_today_record'][player]['nothing']+=1
        pay(gs,data['winner'],data['loser'],point)
def ZHMO(gs,data):
        point=calculate_point(gs,gs.parameters['op']['tai'])
        for player in gs.parameters['player_now']:
                if data['winner'] == player:
                        gs.parameters['player_today_record'][player]['zhmo']+=1
                else:
                        gs.parameters['player_today_record'][player]['bai_mo']+=1
                        pay(gs,data['winner'],player,point)
     
        if data['winner'] != gs.parameters['banker_name']:
                #自摸者不是莊家，莊家要另外付莊家點數
                zhung_bai_mo(gs,data)  
def zhung_bai_mo(gs,data):
        pay(gs,data['winner'],gs.parameters['banker_name'],(gs.parameters['liang']*2+1)*gs.parameters['tai'])     
def ZAHU(gs,data):
        point=calculate_point(gs,gs.parameters['op']['tai'])
        for player in gs.parameters['player_now']:
                if data['winner'] == player:
                        gs.parameters['player_today_record'][player]['gun']+=3
                else:
                        gs.parameters['player_today_record'][player]['hu']+=1
                        pay(gs,player,data['winner'],point) 
        if data['winner'] != gs.parameters['banker_name']:
                #詐胡者不是莊家，莊家另外收莊家點數
                zhung_get_bonus(gs,data)
        else:
                zhung_zahu(gs,data)
def zhung_get_bonus(gs,data):
        pay(gs,gs.parameters['banker_name'],data['winner'],(gs.parameters['liang']*2+1)*gs.parameters['tai'])
def zhung_zahu(gs,data): 
        for player in gs.parameters['player_now']:
                if data['winner'] != player:
                        pay(gs,player,data['winner'],(gs.parameters['liang']*2+1)*gs.parameters['tai'])
        
def THREE_SIANG(gs):
        for win,tai in gs.parameters['op']['tai'].items():
                win_transferd=transfer_string_from_iso88591_to_utf8(win)
                point=calculate_point(gs,tai)
                gs.parameters['player_today_record'][win_transferd]['hu']+=1
                gs.parameters['player_today_record'][gs.parameters['op']['loser']]['gun']+=1
                pay(gs,win_transferd,gs.parameters['op']['loser'],point) 
           
def PONG_NO_PONG(gs,data):
        pay(gs,data['winner'],data['loser'],1)
def liangzhung(gs):
        if gs.parameters['op']['point'][gs.parameters['banker_name']] > 0:
                gs.parameters['liang']+=1
                return 0
        elif gs.parameters['op']['point'][gs.parameters['banker_name']]==0 and "CHAW" in gs.parameters['op']['action']:
                gs.parameters['liang']+=1
                
                if "CHAW" in gs.parameters['op']['action']:
                        for player in gs.parameters['player_now']:
                                gs.parameters['player_today_record'][player]['nothing']+=1
                return 0
        else:
                gs.parameters['fong_idx']+=1
                gs.parameters['liang']=0
                gs.get_banker_name()    
                return 1
     

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        