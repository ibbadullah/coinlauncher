$(document).ready(function(){
    // Desktop profile modal hide/show
    $("#dProfileIcon").on('click',function(){
       $('#dProfileModal').css({"display":"block"});
    });

    $(document).on("click", function(event){
        var $trigger = $("#dProfileIcon");

        if($trigger !== event.target && !$trigger.has(event.target).length){
            $('#dProfileModal').css({"display":"none"});
        }

        });



    // mobile profile modal hide/show
    $("#mProfileIcon").click(function(){
        $('#mProfileModal').css("display","block");
    });


    // Mobile menu modal hide/show
    $("#mMenuIcon").on('click',function(){
       $('#mMenuModal').css({"display":"block"});
    });


    // Mobile signup modal hide/show
    $("#mSignUpLoginIcon").on('click',function(){
       $('#mLoginSignupModal').css({"display":"block"});
    });

    $(document).on("click", function(event){
        var $trigger = $("#mSignUpLoginIcon");

        if($trigger !== event.target && !$trigger.has(event.target).length){
            $('#mLoginSignupModal').css({"display":"none"});
        }

        });


    $('.mobileDialogCloseBtn').click(function () {
        $('.profileModel').css("display","none");
    });
});

