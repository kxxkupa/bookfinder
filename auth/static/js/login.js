$(document).ready(function(){
    // 로그인, 회원가입 input focus
    $("#form .input_box input").on({
        "focusin": function () {
            $(this).siblings().addClass("on");
        },
        "focusout": function () {
            if($(this).val() == ""){
                $(this).siblings().removeClass("on");
            }            
        }
    });
})
