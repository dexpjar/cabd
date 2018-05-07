// Interactiveness now

(function() {

	var clock = document.querySelector('digiclock');
	
	// But there is a little problem
	// we need to pad 0-9 with an extra
	// 0 on the left for hours, seconds, minutes
	
	var pad = function(x) {
		return x < 10 ? '0'+x : x;
	};
	
	var ticktock = function() {
		var d = new Date();
		
		var h = pad( d.getHours() );
		var m = pad( d.getMinutes() );
		var s = pad( d.getSeconds() );
		
		var current_time = [h,m,s].join(':');
		
		if (clock) {
		    clock.innerHTML = current_time;
		}
		
	};
	
	ticktock();
	
	// Calling ticktock() every 1 second
	setInterval(ticktock, 1000);
	
}());

/* ---------- Notifications ---------- */
	$('.noty').click(function(e){
		e.preventDefault();
		var options = $.parseJSON($(this).attr('data-noty-options'));
		noty(options);
	});

$(document).ready(function () {
    $(".tr_table_user").click(function(){
        $("#name_user")[0].innerHTML = $(this).find(".table_first_name")[0].innerHTML + " " + $(this).find(".table_last_name")[0].innerHTML;
        $("#email_user")[0].innerHTML = $(this).find(".table_email")[0].innerHTML;
        $("#active_user")[0].innerHTML = $(this).find(".table_is_active")[0].innerHTML;
        $("#superuser_user")[0].innerHTML = $(this).find(".table_is_superuser")[0].innerHTML;
        var id = $(this).find(".id_user").val();
        $("#link_deleted_user").attr("href","/principal/delete_user_admin_view/"+id);
        $("#link_edit_user").attr("href","/principal/edit_user_admin_view/"+id);
        $("#div_user_deleted").hide();
        $(".register-info-wraper").show();
    });

    $(".tr_table_app").click(function(){
        $("#taskcode_app")[0].innerHTML = $(this).find(".table_taskcode")[0].innerHTML;
        $("#name_app")[0].innerHTML = $(this).find(".table_name")[0].innerHTML;
        $("#citation_app")[0].innerHTML = $(this).find(".table_citation")[0].innerHTML;
        $("#image_app")[0].src = $(this).find(".image_app_table")[0].src;
        $("#image_app")[0].alt = $(this).find(".table_name")[0].innerHTML;
        $("#command_app")[0].innerHTML = $(this).find(".table_command")[0].innerHTML;
        $("#description_app")[0].innerHTML = $(this).find(".table_description")[0].innerHTML;
        var id = $(this).find(".id_app").val();
        $("#link_deleted_app").attr("href","/principal/delete_app_admin_view/"+id);
        $("#link_edit_app").attr("href","/principal/edit_app_admin_view/"+id);
        $("#div_app_deleted").hide();
        $(".register-info-wraper").show();
    });

    $(".tr_table_task").click(function(){
        $("#name_task")[0].innerHTML = $(this).find(".table_name")[0].innerHTML;
        $("#state_task")[0].innerHTML = $(this).find(".table_state")[0].innerHTML;
        $("#creationdate_task")[0].innerHTML = $(this).find(".table_creationdate")[0].innerHTML;
//        $("#input_task")[0].src = $(this).find(".image_app_table")[0].src;
//        $("#output_task")[0].alt = $(this).find(".table_name")[0].innerHTML;
        $("#app_task")[0].innerHTML = $(this).find(".table_app")[0].innerHTML;
        $("#user_task")[0].innerHTML = $(this).find(".table_user")[0].innerHTML;
        $("#taskcode_task")[0].innerHTML = $(this).find(".table_taskcode")[0].innerHTML;
        $(".register-info-wraper").show();
        $('html, body').animate({
            scrollTop: $("#navbar-header").offset().top
        }, 2000);
    });

    $(".tr_table_image").click(function(){
        $("#image_image")[0].src = $(this).find(".image_table")[0].src;
        $(".register-info-wraper").show();
    });

    $(".tr_table_param").click(function(){
        $("#name_param")[0].innerHTML = $(this).find(".table_name")[0].innerHTML;
        $("#state_param")[0].innerHTML = $(this).find(".table_state")[0].innerHTML;
        $("#allowedformat_param")[0].innerHTML = $(this).find(".table_allowedformat")[0].innerHTML;
        $("#app_param")[0].innerHTML = $(this).find(".table_app")[0].innerHTML;
        $("#required_param")[0].innerHTML = $(this).find(".table_required")[0].innerHTML;
        $("#value_param")[0].innerHTML = $(this).find(".table_value")[0].innerHTML;
        $("#info_param")[0].innerHTML = $(this).find(".table_info")[0].innerHTML;
        $("#option_param")[0].innerHTML = $(this).find(".table_option")[0].innerHTML;
        $("#input_param")[0].innerHTML = $(this).find(".table_input")[0].innerHTML;
        $("#output_param")[0].innerHTML = $(this).find(".table_output")[0].innerHTML;
        $(".register-info-wraper").show();
    });

    $(".tr_table_section").click(function(){
        $("#title_section")[0].innerHTML = $(this).find(".table_title")[0].innerHTML;
        $("#app_section")[0].innerHTML = $(this).find(".table_app")[0].innerHTML;
        $("#description_section")[0].innerHTML = $(this).find(".table_description")[0].innerHTML;
        $(".register-info-wraper").show();
    });

    $(".link_deleted_image").click(function(){
        $("#image_deleted").show();
    });

    $(".table-register-info").hide();
});

