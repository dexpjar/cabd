$(document).ready(function(){
  $("#confirmPassword").change(function(){
     if($(this).val()!=$("#id_register-password").val()){
        $(this).val("");
        $(this).css("border-color", "red");
        $("#error_confirm_password").show();
     }
     else{
        $(this).css("border-color", "#D3D3D3");
        $("#error_confirm_password").hide();
     }
  });
  $("#id_register-email").change(function(){
     if($(this).val()!=""){
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        var result = regex.test($(this).val());
        if(result == false){
            $(this).css("border-color", "red");
            $("#error_email").show();
        }
        else{
            $(this).css("border-color", "#D3D3D3");
            $("#error_email").hide();
            $("#id_register-username").val($(this).val());
        }
     }
  });
  $("#id_register-password").change(function(){
     var regex = /^(?=.*[a-z])[A-Za-z0-9\d=!\-@._*]+$/;
     if($(this).val().length < 8){
        $(this).css("border-color", "red");
        $("#error_password_length").show();
        $("#error_password_format").hide();
     }
     else{
        var result = regex.test($(this).val()) && /[a-z]/.test($(this).val()) && /\d/.test($(this).val());
        if(result == false){
            $(this).css("border-color", "red");
            $("#error_password_length").hide();
            $("#error_password_format").show();
        }
        else{
            $(this).css("border-color", "#D3D3D3");
            $("#error_password_length").hide();
            $("#error_password_format").hide();
        }
     }
  });
  $("#button_register").click(function(event){
     /*First Name*/
     if($("#id_register-first_name").val()==""){
        event.preventDefault();
        $("#id_register-first_name").css("border-color", "red");
        $("#error_first_name_required").show();
     }
     else{
        $("#id_register-first_name").css("border-color", "#D3D3D3");
        $("#error_first_name_required").hide();
     }

     /*Last Name*/
     if($("#id_register-last_name").val()==""){
        event.preventDefault();
        $("#id_register-last_name").css("border-color", "red");
        $("#error_last_name_required").show();
     }
     else{
        $("#id_register-last_name").css("border-color", "#D3D3D3");
        $("#error_last_name_required").hide();
     }

     /*Email*/
     if($("#id_register-email").val()==""){
        event.preventDefault();
        $("#id_register-email").css("border-color", "red");
        $("#error_email_required").show();
     }
     else{
        $("#id_register-email").css("border-color", "#D3D3D3");
        $("#error_email_required").hide();
     }

     /*Institution*/
     if($("#id_profile-institution").val()==""){
        event.preventDefault();
        $("#id_profile-institution").css("border-color", "red");
        $("#error_institution_required").show();
     }
     else{
        $("#id_profile-institution").css("border-color", "#D3D3D3");
        $("#error_institution_required").hide();
     }

     /*Password*/
     if($("#id_register-password").val()==""){
        event.preventDefault();
        $("#id_register-password").css("border-color", "red");
        $("#error_password_required").show();
     }
     else{
        $("#id_register-password").css("border-color", "#D3D3D3");
        $("#error_password_required").hide();
     }

     /*Confirm Password*/
     if($("#confirmPassword").val()==""){
        event.preventDefault();
        $("#confirmPassword").css("border-color", "red");
        $("#error_confirm_password_required").show();
     }
     else{
        $("#confirmPassword").css("border-color", "#D3D3D3");
        $("#error_confirm_password_required").hide();
     }
  });
});