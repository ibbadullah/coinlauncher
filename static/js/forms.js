$(document).ready(function () {
        $('.infoDiv').click(function () {
            $('.rightDiv').animate({right:"0%"});
        });

        $('.leftDiv').click(function () {
            $('.rightDiv').animate({right:"-200%"});
        });
    });
