// HTMLが読み込まれてから実装
document.addEventListener("DOMContentLoaded", function () { 

    let jqxhr;
    $('.submit').on('click', function(){
        event.preventDefault();
        if (jqxhr) {
            return;
        }
        jqxhr = $.ajax({
            url: '/add_favorite',
            type: 'post',
            data: $(this).parent('form').serialize(),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
})