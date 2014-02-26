function loadComments(id, type) {
    $('#comment-list').show();
    $.ajax({
        type: 'GET',
        cache: false,
        url: '/comments/?'+type+'_id'+'='+id,
        beforeSend: function () {
            $('#comment-list').html('<div class="text-center">' +
                '<div class="page-header">' +
                '<h3>Loading Comments</h3>' +
                '</div>' +
                '<img src="/static/img/ajax-loader.gif"/>' +
                '</div>'
            );
        },
        success: function (data) {
            $('#comment-list').html(data);

        }
    });
}