
import json
from py.common.sql_log_operation import *
import sys    
#sys.stdout.reconfigure(encoding='utf-8')
def do_restore(gs):
        ret_obj={
                "gs":"",
                "log":[]
        }
        
        if gs.get_latest_gs()==1:
               ret_obj["log"]=sql_get_log(gs.log_dbname)
        ret_obj["gs"]=gs.parameters
                
        
        #print(json.dumps(gs.parameters, indent=4))
        #print(ret_obj)
        return  json.dumps(ret_obj)
