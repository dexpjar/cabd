$(document).ready(function(){
    $("#email").change(function(){
     if($(this).val()!=""){
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        var result = regex.test($(this).val());
        if(result == false){
            $(this).css("border-color", "red");
            $("#error_email_format").show();
        }
        else{
            $(this).css("border-color", "#D3D3D3");
            $("#error_email_format").hide();
        }
     }
    });
    $("#button_send_message").click(function(event){
     /*First Name*/
         if($("#name").val()==""){
            event.preventDefault();
            $("#name").css("border-color", "red");
            $("#error_firstname_required").show();
         }
         else{
            $("#name").css("border-color", "#D3D3D3");
            $("#error_firstname_required").hide();
         }
         /* Email */
         if($("#email").val()==""){
            event.preventDefault();
            $("#email").css("border-color", "red");
            $("#error_email_required").show();
         }
         else{
            $("#email").css("border-color", "#D3D3D3");
            $("#error_email_required").hide();
         }
         /* Subject */
         if($("#subject").val()==""){
            event.preventDefault();
            $("#subject").css("border-color", "red");
            $("#error_subject_required").show();
         }
         else{
            $("#subject").css("border-color", "#D3D3D3");
            $("#error_subject_required").hide();
         }
         /* Message */
         if($("#message").val()==""){
            event.preventDefault();
            $("#message").css("border-color", "red");
            $("#error_message_required").show();
         }
         else{
            $("#message").css("border-color", "#D3D3D3");
            $("#error_message_required").hide();
         }

     });
});