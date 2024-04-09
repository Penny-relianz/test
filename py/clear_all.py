import json

from py.common.globalstuff import get_now_time_str
def do_clear_all(gs):
        t=get_now_time_str()
        gs.create_new_gs(t)
        gs.create_new_log_table_in_sql()
        #sql clear today
        print(json.dumps(gs.parameters, indent=4))
        return json.dumps(gs.parameters)