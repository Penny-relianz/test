
function jiang_btn_init(){
	
	$('#btnNew4,#btnNew2,#btnNew1').on('click',function(){
		//obj={"firstName":"John", "lastName":"Doe"}
                //console.log("aaaa"+gs.fong_idx)
                
                if(player_input_is_illegal()==0){
                        var date_str=Get_now_time();
                        data={
                                "circle"        :$(this).attr('circle'),
                                "time"          :date_str,
                                "jiang"         :gs.jiang,
                                "start_position":$("#selLocation").val(),
                                "p_0"           :$('#p_dong').val(),
                                "p_1"           :$('#p_nan').val(),
                                "p_2"           :$('#p_si').val(),
                                "p_3"           :$('#p_bai').val()
                        }
						console.log(data)
                        send_to_server('NewJiang',data);
                        
                }
	})
}
function player_input_is_illegal(){
        player_on_the_ground=[];
        var error=0;
        for (i = 0; i < $('.player_on_the_ground_input').length; i++){
                if($('.player_on_the_ground_input')[i].value==""){
                        alert('登入失敗，請輸入四位玩家');
                        console.log('登入失敗，請輸入四位玩家');
                        return 1;
                }
               
                player_on_the_ground.forEach(function(player_on_the_ground_sign, index_sign){
                        if($('.player_on_the_ground_input')[i].value==player_on_the_ground_sign){
                                alert('玩家 '+player_on_the_ground_sign+' 重複登入');
                                console.log('玩家 '+player_on_the_ground_sign+' 重複登入');
                                error=1;
                        }
                });
                player_on_the_ground.push($('.player_on_the_ground_input')[i].value);
        }
        if (error)
                return 1;
        else{
                player_on_the_ground.forEach(function(player_on_the_ground_sign, index_sign){
                        console.log("玩家 : "+$('.player_on_the_ground_input')[index_sign].value+"　登入成功"); 
                })
                return 0;
        } 
}

function newjiang_update(gs_obj_from_server){
        gs=JSON.parse(gs_obj_from_server);  
        console.log(gs);
        Update_Record_Table();
        Update_Title();
        switch_Button();
        restore_selector_table(gs);
        give_table_selector_css_attr();
        append_log_table();
        
}
/*
function create_table_selector(){
        $('#tblSelHUGUN tbody tr').remove();
        for (i = 0; i < $('.player_on_the_ground_input').length; i++){
                player_on_the_ground_name=$('.player_on_the_ground_input:eq('+i+')').val() 
                $('#tblSelHUGUN tbody').append('<tr id="trPlayer_'+i+'"><td id="tdPlayerHu_'+i+'" class="tblSelHU">'+player_on_the_ground_name+'</td><td id="tdPlayerGun_'+i+'" class="tblSelGUN">'+player_on_the_ground_name+'</td></tr>');
	}
        return 0;
}*/

function give_table_selector_css_attr(){
	var color_hu="#28a745";
	var color_gun="#dc3545";
	$('.tblSelHU').hover(function(){
		$(this).css('background-color',color_hu).css("cursor","pointer");
	}, function() {
		if (!$(this).hasClass('sel_winner'))
			$(this).css('background-color', '').css("cursor","default");
	}).click(function(){
		$('.tblSelHU').css("background-color","").removeClass('sel_winner');
		$(this).css('background-color',color_hu);
		if ($(this).hasClass('sel_winner'))
			$(this).removeClass('sel_winner');
		else
			$(this).addClass('sel_winner');
		console.log("click HU");
	});
	
	$('.tblSelGUN').hover(function(){
		$(this).css('background-color',color_gun).css("cursor","pointer");;
	},function() {
		if (!$(this).hasClass('sel_loser'))
			$(this).css('background-color', '').css("cursor","default");;
	}).click(function(){
		$('.tblSelGUN').css("background-color","").removeClass('sel_loser');
		$(this).css('background-color',color_gun);

		if ($(this).hasClass('sel_loser'))
			$(this).removeClass('sel_loser');
		else
			$(this).addClass('sel_loser');
		console.log($(this).siblings());
	});
        return 0;
}








