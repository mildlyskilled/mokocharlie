function displayCommentForm() {
    $('#comment-form').show();
    $.ajax({
        type: 'GET',
        cache: false,
        url: '/comments/new_form/',
        beforeSend: function(){
            $('#comment-form').html('<img src="/static/img/ajax-loader.gif"/>');
        },
        success: function (data) {
            $('#comment-form').html(data);
            $('html, body').animate({
                scrollTop: $("#comment-form").offset().top
            }, 1000);
        }
    });
}