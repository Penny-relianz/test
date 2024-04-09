
function Excel_save_btn_init(){
	
	$('#btnExcel_save').on('click',function(){
                var r=confirm("確認是否關閉EXCEL檔案，更新完excel後必須清空目前的戰績?");
                if (r!=true){
                        return 1;
                }		  
		
                send_to_server('excel_save',gs)
	})
}

function excel_save(gs_obj_from_server){
        ret=JSON.parse(gs_obj_from_server);  
        if (ret['ret']==0)
                alert('Save OK.');
        else if(ret['ret']==1)    
                alert('Save Fail.');
        else
                alert("unknown error."+ret);
}