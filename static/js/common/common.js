var FONG=['東起','東二','東三','東底','南起','南二','南三','南底','西起','西二','西三','西底','北起','北二','北三','北底'];
var TWOFONG=['中起','中二','中三','中底','發起','發二','發三','發底'];
function send_to_server(event,data){
        socket.emit(event,data);   
}
/*function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
  }*/
function listen_from_server(event,callback_function){
        socket.on(event,callback_function)
}

function gs_init(){
        send_to_server('gs_init',"")
        
}
function selector_table_init(){
        $('#tblSelHUGUN tbody tr').remove();
}
function log_table_init(){
        $('#tblShowDetail tbody tr').remove();
	$('#tblShowDetail tbody').append('<tr></tr>');
        $('#tblShowDetail thead tr').remove();
        $('#tblShowDetail thead').append('<tr><th id=\'LOG_DATE\' colspan="5">LOG</th></tr>')
}
function socket_init(){
        listen_from_server('update_dashboard_action',function(gs_obj_from_server) {action_update(gs_obj_from_server)})
        listen_from_server('update_dashboard_newjiang',function(gs_obj_from_server) {newjiang_update(gs_obj_from_server)})
        listen_from_server('restore',function(gs_obj_from_server) {restore(gs_obj_from_server)})
        listen_from_server('gs_init',function(gs_obj_from_server) {gs_init_callback(gs_obj_from_server);})
		listen_from_server('clear_all',function(gs_obj_from_server) {clear_all(gs_obj_from_server)})
		listen_from_server('excel_save',function(gs_obj_from_server) {excel_save(gs_obj_from_server)})
        listen_from_server('clear_last',function(gs_obj_from_server) {restore(gs_obj_from_server)})
       
        
}
function socket_init_obs(){
        listen_from_server('updateobs',  function(gs_obj_from_server) {
                update_OBS(gs_obj_from_server);
        });
        listen_from_server('show_current_point_animate',  function(gs_obj_from_server) {
			update_obs_gs(gs_obj_from_server);
			stop_point_animate();
			show_point_animate();
		});
		listen_from_server('open_popup_window',  function(gs_obj_from_server) {
			update_obs_gs(gs_obj_from_server);
			/*if (gs.fong_idx==16){
				test_popup()
			}*/
		});
		listen_from_server('clsoe_popup_window',  function(gs_obj_from_server) {
			update_obs_gs(gs_obj_from_server);
			test_popup()
		});
		listen_from_server('get_popup_window_info',  function(popinfo) {
			update_popup_info(popinfo,10,1);
			//console.log("gg");
		});
}
function gs_init_callback(gs_obj_from_server){
        gs_obj_from_server=JSON.parse(gs_obj_from_server);  
        gs=gs_obj_from_server;
        console.log("gs init complete.");
}




function Enable_Action_Button(){
	$(".playing").removeClass('disabled').prop('disabled','');
	$(".non_playing").prop('disabled','disabled').addClass('disabled');
}
function Diable_Action_Button(){
	$(".playing").addClass('disabled').prop('disabled','disabled');
	$(".non_playing").prop('disabled','').removeClass('disabled');
}


function Check_is_end(){
	if(gs.fong_idx==gs.circle*4){
		alert("本將結束，沒有任何動作");
		Diable_Button();
		return 0;
	}else
		return 1;
}
function Get_now_time(){
	var date = new Date();
	var date_str=(date.getMonth()+1)+"/"+date.getDate()+" "+date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
	return date_str;
}

function Update_Title(){
	$("#LOG_TABLE_THEAD tr").remove();
	if(gs.fong_idx>=gs.circle*4 || gs.player_now[0] == undefined){
		$('#title_giang').text("結束 第"+ gs.jiang +" 將");
		$("#LOG_TABLE_THEAD").append("<tr><th colspan='5'>"+"結束 第"+ gs.jiang +" 將"+"</th></tr>")
		
	}else{
		$('#title_giang').show().text("第"+gs.jiang+"將 - "+FONG[gs.fong_idx]);	
		$("#LOG_TABLE_THEAD").append("<tr><th>"+FONG[gs.fong_idx]+"-連"+gs.liang+"</th><th>"+gs.player_now[0]+"</th><th>"+gs.player_now[1]+"</th><th>"+gs.player_now[2]+"</th><th>"+gs.player_now[3]+"</th></tr>")
		
	}
	if(gs.liang>0){
		$('#title_lieng').show().text(" - 莊家 連"+gs.liang);
	}else{
		$('#title_lieng').hide();
	}	
	return 0
}
function append_log_table(){
        
		tmp_liang=cur_state.liang
		tmp_fong=cur_state.fong_idx%16
		
		if(gs.op.hasOwnProperty('circle')){
                $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+gs.jiang+'_jiang"><td>'+gs.op.time+'第'+gs.jiang+'將開始</td><td id='+gs.player_now[0]+'_'+gs.jiang+'>東-'+gs.player_now[0]+'</td><td id='+gs.player_now[1]+'_'+gs.jiang+'>南-'+gs.player_now[1]+'</td><td id='+gs.player_now[2]+'_'+gs.jiang+'>西-'+gs.player_now[2]+'</td><td id='+gs.player_now[3]+'_'+gs.jiang+'>北-'+gs.player_now[3]+'</td></tr>' );	
                return
        }
        if(tmp_liang>0){
                $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+FONG[tmp_fong]+'liang'+tmp_liang+'"><td>'+gs.op.time+FONG[tmp_fong]+'連'+tmp_liang+'</td><td>'+gs.op.point[gs.player_now[0]]+'</td><td>'+gs.op.point[gs.player_now[1]]+'</td><td>'+gs.op.point[gs.player_now[2]]+'</td><td>'+gs.op.point[gs.player_now[3]]+'</td></tr>' );
        }else{
                $('#tblShowDetail > tbody > tr:first').before( '<tr id="'+FONG[tmp_fong]+'"><td>'+gs.op.time+FONG[tmp_fong]+'</td><td>'+gs.op.point[gs.player_now[0]]+'</td><td>'+gs.op.point[gs.player_now[1]]+'</td><td>'+gs.op.point[gs.player_now[2]]+'</td><td>'+gs.op.point[gs.player_now[3]]+'</td></tr>' );
        }
        //$('#tblSelHUGUN tbody').append('<tr id="trPlayer_'+index+'"><td id="tdPlayerHu_'+index+'" class="tblSelHU">'+player_on_the_ground_name+'</td><td id="tdPlayerGun_'+index+'" class="tblSelGUN">'+player_on_the_ground_name+'</td></tr>');
}		

function sort_record_by_point(Current_Record){
	var sortable=[];
	var sorted_obj={};
	$.each(Current_Record, function(player_on_the_ground_name,player_on_the_ground_obj) {
		player_on_the_ground_obj.name=player_on_the_ground_name;
		sortable.push(player_on_the_ground_obj);
	}); 
	sortable.sort(function(a, b){
		var a1= a.point, b1= b.point;
		if(a1==b1) return -1;
		return a1> b1? 1: -1;
	});
	sortable.reverse();
	sortable.forEach(function(element){
	  sorted_obj[element.name]=element;
	});
	return sorted_obj;
}
function sort_popup_info_point(a, b) {
    if (a[2] === b[2]) {
        return 0;
    }
    else {
        return (a[2] < b[2]) ? -1 : 1;
    }
}

function Update_Record_Table(){
	console.log("---目前所有玩家的記錄戰績---\n");
	console.log(gs.player_today_record);
	console.log("----------------------------\n");
	gs.player_today_record=sort_record_by_point(gs.player_today_record);
	$('#tblPlyerRecord > tbody > tr').remove();
	var i=0;
	$.each(gs.player_today_record,function(name,value){
		$('#tblPlyerRecord > tbody ').append( '<tr><td id='+name+'_record_name'+' colspan=1>'+name+'</td><td id='+name+'_record_point'+'>'+value.point+'</td><td id='+name+'_record_zhmo'+'>'+value.zhmo+'</td><td id='+name+'_record_hu'+'>'+value.hu+'</td>><td id='+name+'_record_gun'+'>'+value.gun+'</td><td id='+name+'_record_playjiang'+'>'+value.playjiang+'</td></tr>' );
		i++;
	});
}

function switch_Button(){
	if(gs.fong_idx >= gs.circle*4 || gs.jiang==0 ){
		Diable_Action_Button();
	}else{
		Enable_Action_Button();
		
	}
}



