$(document).ready(function() {
    $('#new-item-submit').click(function(e) {
        e.preventDefault();
        var text = $('#new-list-item-text').val();
        if (text) {
            var url = "/list/create";
            var data = {"text":text};
            postRequest(url, data);
        } else {
            alertError("Item text should not be empty.");
        }
    });
    $('.edit-button').click(function(e) {
        e.preventDefault();
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        if (text) {
            var url = "/list/" + itemId + "/edit";
            var data = {"text": text};
            putRequest(url, data);
        } else {
            alertError("Item text should not be empty.");
        }
    });
    $('.delete-button').click(function(e) {
        e.preventDefault();
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var url = "/list/" + itemId + "/delete";
        var data = {};
        deleteRequest(url, data);
    });
});
