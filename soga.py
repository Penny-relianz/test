# -*- coding: utf-8 -*-
import sys    
sys.stdout.reconfigure(encoding='utf-8')

import os
import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import send_from_directory

from py.newjiang import *
from py.do_action import *
from py.clear_last import *
from py.clear_all import *
from py.restore import *
from py.do_excel_save import *
from py.do_statistic_db_update import *
from py.common.globalstuff import globalstuff
gs=globalstuff()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
#import approute
#import socketevent
@app.route('/')
def websocket_example():
    return render_template('websocket.html')
    
@app.route('/dashboard')
def SogaDashboard():
    return render_template('dashboard.html')
    
@app.route('/obs')
def ShowOBS():
    return render_template('obs.html')
    
@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/image/icon'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
    
'''
@socketio.on('connection complete')
def handle_my_custom_event(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        print('Send ggg event to client...')
        #socketio.emit('ggg', json, callback=messageReceived)
'''

@socketio.on('gs_init')
def gs_init(data):
        gs.__init__()
        ret_obj=json.dumps(gs.parameters)
        socketio.emit('gs_init',ret_obj,broadcast=True)
@socketio.on('do_action')
def action_handle(data):
        ret_obj=do_action(gs,data)
        socketio.emit('updateobs',ret_obj,broadcast=True)
        socketio.emit('show_current_point_animate',ret_obj,broadcast=True)
        socketio.emit('update_dashboard_action',ret_obj,broadcast=True)
        socketio.emit('open_popup_window',ret_obj,broadcast=True)
@socketio.on('clear_last')
def clear_last(data):
        ret_obj=do_clear_last(gs)
        socketio.emit('updateobs',ret_obj,broadcast=True)
        socketio.emit('clear_last',ret_obj,broadcast=True)
@socketio.on('clear_all')
def clear_all(data):
        #print(data)
        ret_obj=do_clear_all(gs)
        socketio.emit('updateobs',ret_obj,broadcast=True)
        socketio.emit('clear_all',ret_obj,broadcast=True)
@socketio.on('excel_save')
def excel_save(data):
        #print(data)
        ret_obj=do_excel_save(data)
        do_statistic_db_update(data)
        socketio.emit('excel_save',ret_obj,broadcast=True)        
@socketio.on('NewJiang')
def newjiang_handle(data):
        print(data)
        #print(data['p_0'].encode('utf8'))
        #data=json.loads(data,encoding='utf-8')
        #print (data)
        #rint(data['p_0'].encode('big5'))
        #print(data['p_0'].unicode())
        ret_obj=newjiang_setting(gs,data)
        
        socketio.emit('updateobs',ret_obj,broadcast=True)
        socketio.emit('update_dashboard_newjiang',ret_obj,broadcast=True)
        socketio.emit('close_popup_window',ret_obj,broadcast=True)
@socketio.on('restore')
def restore(data):
        print("你好"+data)
        ret_obj=do_restore(gs)
        socketio.emit('updateobs',ret_obj,broadcast=True)
        socketio.emit('restore',ret_obj,broadcast=True)

@socketio.on('get_popup_window_info')
def get_popup_window_info(data):
        print("你好 get_popup_window_info"+data)
        ret=get_info_from_statistic_db()
        socketio.emit('get_popup_window_info',ret,broadcast=True)


if __name__ == '__main__':
        socketio.run(app,host="0.0.0.0",debug=True)
