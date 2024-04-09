import json
from py.common.sql_log_operation import *

def do_clear_last(gs):
        
        print("clear last.....")
        #last_gs=get_last_log_and_remove_it(gs.parameters['starttime'])
        sql_clear_last(gs.log_dbname)
        gs.get_latest_gs()
        ret_obj={
                "gs":gs.parameters,
                "log":sql_get_log(gs.log_dbname)
        }
        
                
        
        #print(json.dumps(gs.parameters, indent=4))
        #print(ret_obj)
        return  json.dumps(ret_obj)
    