
function clear_all_btn_init(){
	
	$('#btnClear_all').on('click',function(){
                var r=confirm("確定是否已經存入EXCEL，你確定要清除全部?");
                if (r!=true){
                        return 1;
                }
				  
		data={
                        "action":"clearall"
                }
                send_to_server('clear_all',data)
	})
}

function clear_all(gs_obj_from_server){
        gs=JSON.parse(gs_obj_from_server);  
        console.log(gs);
        Update_Record_Table();
        Update_Title();
        switch_Button();
        log_table_init();
        selector_table_init();
}