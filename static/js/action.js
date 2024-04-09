
function action_btn_init(){
	
	$('.do_action').on('click',function(){
                var Winner_name=$('.sel_winner').text();
                var Loser_name=$('.sel_loser').text();
                var Tai=get_tai($(this).attr('tai'));
                var date_str=Get_now_time();
                
                
                if(check_action_illegal(Winner_name,Loser_name,Tai,$(this).val())==0){
                        console.log($(this).val())
                        if ($(this).val().indexOf("三響")!=-1){
                                
                                three_gun_handle($(this),Winner_name,Loser_name,Tai,date_str)
                        }else{
                                //console.log(Tai)
                                data={
                                        "action":$(this).attr('id'),
                                        "time":date_str,
                                        "winner":Winner_name,
                                        "loser":Loser_name,
                                        "tai":Tai,
                                        "fong_idx":gs.fong_idx,
                                        "liang":gs.liang
                                }
                                send_to_server('do_action',data)
                        }
                        
		}
	});
        
        
}
function action_update(gs_obj_from_server){
        gs=JSON.parse(gs_obj_from_server);  
        console.log(gs);
        Update_Record_Table();
        Update_Title();
        switch_Button();
        if(gs.fong_idx<=(gs.circle*4)){
                append_log_table();
                cur_state.liang=gs.liang
                cur_state.fong_idx=gs.fong_idx
        }
}
function three_gun_handle(this_,win,lose,tai,date_str){
        console.log(this_)
        console.log(win)
        console.log(lose)
        console.log(tai)
        console.log(date_str)
        if(this_.val().indexOf("1")!=-1){
                gs.threepong_tai={}
                gs.threepong_tai[win]=tai
                this_.val('三響-2')
        }else if(this_.val().indexOf("2")!=-1){
                gs.threepong_tai[win]=tai
                this_.val('三響-3')
        }else if(this_.val().indexOf("3")!=-1){
                gs.threepong_tai[win]=tai
                data={
                        "action":this_.attr('id'),
                        "time":date_str,
                        "winner":win,
                        "loser":lose,
                        "tai":gs.threepong_tai,
                        "fong_idx":gs.fong_idx,
                        "liang":gs.liang
                }
                send_to_server('do_action',data)
                this_.val('三響-1')
        }
        
        
}
function get_tai(attr_tai){
        var Tai;
        //console.log(attr_tai)
        if (attr_tai==undefined)
                Tai=$('#selTai').val();
        else 
                Tai=attr_tai;
        Tai=parseInt(Tai);
        if(Tai==""){
                Tai=0;
        }
        //console.log("tai"+typeof(Tai))
        return Tai;
}

function check_action_illegal(Winner_name,Loser_name,Tai,action){
        // action.indexOf("摸")!=-1 找到摸 ->是自摸
        //console.log(action)
        if(Check_is_end()==0)
                return 1;
       
        if(Winner_name=="" && action!="臭莊"){
                alert('誰胡拉?');
                return 1;
        }
        if(Loser_name=="" && action.indexOf("摸")==-1 && action!="詐胡" && action!="臭莊"){
                alert('誰放槍拉?');
                return 1;
        }
        if(Winner_name==Loser_name && action.indexOf("摸")==-1 && action!="詐胡" && action!="臭莊"){
                alert('自己胡自己');
                return 1;
        }
        //console.log("tai"+typeof(Tai))
        if(typeof(Tai)!="number" && action!="臭莊"){
                alert('胡幾台拉!');
                return 1;
        }
        if (Tai==0 &&  action.indexOf("摸")!=-1){
                alert('你媽摸0台!');
                return 1;
        }
        return 0;
        
}