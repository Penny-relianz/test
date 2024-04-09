
function clear_last_btn_init(){
	$('#btnClear_last').on('click',function(){
                data={
                        "action":"clearlast"
                }
                send_to_server('clear_last',data)
	})
}
