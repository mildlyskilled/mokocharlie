function addKeyPair(idx) {
    $('#meta').append(
        '<div class="form-group" id="group_' + idx + '">' +
            '<label for="key_' + idx + '" class="control-label col-lg-3">Description</label>' +
            '<div class="controls col-lg-3 login-fields">' +
            '<input type="text" class="textinput col-lg-12 form-control" placeholder="eg. price" id="key_' +
            idx + '" name="key_' + idx + '"/>' +
            '</div>' +

            '<div class="controls col-lg-3 login-fields">' +
            '<input type="text" class="textinput col-lg-12 form-control" placeholder="eg. GHC 3,000" id="value_' +
            idx + '" name="value_' + idx + '"/>' +
            '</div>' +
            '<div class="controls col-lg-3 login-fields" id="adder_remover_' + idx + '">' +
            '<a id="adder_' + idx + '" onclick="addKeyPair(' + (idx + 1) + ');removeAdder(' + idx + ');" class="btn btn-success">' +
            '<i class="glyphicon glyphicon-plus"></i></a>' +
            '</div>' +
            '</div>'
    );
}

function removeAdder(idx) {
    var removeBtn = '<a id="remover_' + idx + '" onclick="removeKeyPair(' + (idx) + ');removeAdder(' + idx + ');" ' +
        'class="btn btn-danger">' +
        '<i class="glyphicon glyphicon-minus"></i></a>' +
        '</div>';
    $('#adder_remover_' + idx).html(removeBtn);
}

function removeKeyPair(idx) {
    $('#group_' + idx).fadeOut('slow', function(){
        $('#group_' + idx).remove()
    });
}