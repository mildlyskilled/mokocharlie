function toggleCommentForm(image_id) {
    if ($('#comment-form').css('display') == 'none') {
        $('#comment-form').show();
        $.ajax({
            type: 'GET',
            cache: false,
            url: '/comments/new_form/?image_id=' + image_id,
            beforeSend: function () {
                $('html, body').animate({
                    scrollTop: $("#comment-form").offset().top - 20
                }, 1000);

                $('#comment-form').html('<img src="/static/img/ajax-loader.gif"/>');
            },
            success: function (data) {
                $('#comment-form').html(data);
            }
        });
    } else {
        $("#comment-form").html('').hide()
    }
}

function postComment(form) {
    $.ajax({
        type: 'POST',
        cache: false,
        url: '/comments/new_form/',
        data: $('#' + form).serialize(),
        beforeSend: function () {
            $('html, body').animate({
                scrollTop: $("#comment-form").offset().top - 20
            }, 1000);

            $('#comment-form').html('<img src="/static/img/ajax-loader.gif"/>');
        },
        success: function (data) {
            toggleCommentForm(data.image_id);
            loadComments(data.image_id, 'image');
        },
        error: function (data) {
            var obj = $.parseJSON(data.responseText)
            var res = '<div class="alert alert-danger">';
            for (var x = 0; x < obj.image_comment.length; x++) {
                res += '<br />' + obj.image_comment[x];
            }
            res += '</div>';
            $('#comment-form').html(res);
            setTimeout(function () {
                $('#comment-form').fadeOut(500)
            }, 10000);
        }
    });
}

function favouritePhoto(id) {
    $.ajax({
        type: 'GET',
        cache: false,
        url: '/photos/favourite/' + id,
        beforeSend: function () {
            $('#like-button').html('<img src="/static/img/ajax-loader-small.gif"/>');
        },
        success: function (data) {
            $('#like-button').html('<span class="glyphicon glyphicon-heart"></span>');
            $('#like-button').attr('title', 'Click here to remove this image to your favourites');
            $('#like-button').attr('data-original-title', 'Click here to remove this image to your favourites');
            $('#like-button').attr('onclick', "unfavouritePhoto("+id+")");
            $('#like-button').tooltip();
            var obj = $.parseJSON(data)
            if (obj.status == 'failed') {
                alert(obj.message)
            } else {
                $('#like-button').html('<span class="glyphicon glyphicon-heart"></span>');
            }
        },
        error: function (data) {
            $('#like-button').html('<span class="glyphicon glyphicon-heart-empty"></span>');
        }
    });
}

function unfavouritePhoto(id) {
    $.ajax({
        type: 'GET',
        cache: false,
        url: '/photos/unfavourite/' + id,
        beforeSend: function () {
            $('#like-button').html('<img src="/static/img/ajax-loader-small.gif"/>');
        },
        success: function (data) {
            $('#like-button').html('<span class="glyphicon glyphicon-heart-empty"></span>');
            $('#like-button').attr('title', 'Click here to add this image to your favourites');
            $('#like-button').attr('data-original-title', 'Click here to add this image to your favourites');
            $('#like-button').attr('onclick', "favouritePhoto("+id+")");
            var obj = $.parseJSON(data)
            if (obj.status == 'failed') {
                alert(obj.message)
            } else {
                $('#like-button').html('<span class="glyphicon glyphicon-heart-empty"></span>');
            }
        },
        error: function (data) {
            $('#like-button').html('<span class="glyphicon glyphicon-heart"></span>');
        }
    });
}