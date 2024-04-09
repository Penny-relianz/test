function request_restore(){
        send_to_server('restore','restore')
}


function restore(gs_obj_from_server){
        obj=JSON.parse(gs_obj_from_server);  
        gs=obj.gs
        log=obj.log
        console.log(gs);
        Update_Record_Table();
        Update_Title();
        switch_Button();
        log_table_init();
        restore_log_table(log);
        restore_selector_table(gs);
        give_table_selector_css_attr();
        cur_state.liang=gs.liang
	cur_state.fong_idx=gs.fong_idx%16
}

function  restore_log_table(logs){
        console.log(logs)
        logs.forEach(function(log){
                p1=Object.keys(log['point'])[0];
                p2=Object.keys(log['point'])[1];
                p3=Object.keys(log['point'])[2];
                p4=Object.keys(log['point'])[3];
                if (log.action.indexOf("new")==-1){
                        if(log.liang>0){
                                $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+FONG[log.fong_idx]+'"><td>'+log.time+FONG[log.fong_idx]+'連'+log.liang+'</td><td>'+log.point[p1]+'</td><td>'+log.point[p2]+'</td><td>'+log.point[p3]+'</td><td>'+log.point[p4]+'</td></tr>' );
                        }else{
                                $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+FONG[log.fong_idx]+'"><td>'+log.time+FONG[log.fong_idx]+'</td><td>'+log.point[p1]+'</td><td>'+log.point[p2]+'</td><td>'+log.point[p3]+'</td><td>'+log.point[p4]+'</td></tr>' );
                        }
                }else{
                        $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+gs.jiang+'_jiang"><td>'+log.time+'第'+gs.jiang+'將開始</td><td id='+p1+'_'+gs.jiang+'>東-'+p1+'</td><td id='+p2+'_'+gs.jiang+'>南-'+p2+'</td><td id='+p3+'_'+gs.jiang+'>西-'+p3+'</td><td id='+p4+'_'+gs.jiang+'>北-'+p4+'</td></tr>' );	
                }
        });
}

function restore_selector_table(gs){
        player_on_the_ground=gs.player_now
        $('#tblSelHUGUN tbody tr').remove();
	player_on_the_ground.forEach(function(player_on_the_ground_name, index){
		$('#tblSelHUGUN tbody').append('<tr id="trPlayer_'+index+'"><td id="tdPlayerHu_'+index+'" class="tblSelHU">'+player_on_the_ground_name+'</td><td id="tdPlayerGun_'+index+'" class="tblSelGUN">'+player_on_the_ground_name+'</td></tr>');	
	});	
}