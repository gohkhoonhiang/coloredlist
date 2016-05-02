$(document).ready(function() {
    $('.edit-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        var url = "/list/" + itemId + "/edit";
        console.log(url);
        $.ajax({
            type: "PUT",
            url: url,
            dataType: "json",
            data: {"id": itemId, "text": text},
            statusCode: {
                200: function(xhr) {
                    alert("Item updated successfully");
                },
                404: function(xhr) {
                    alert("Item ID not found");
                },
            },
        });
    });
    $('.delete-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        var url = "/list/" + itemId + "/delete";
        console.log(url);
        $.ajax({
            type: "DELETE",
            url: url,
            dataType: "json",
            data: {},
            statusCode: {
                200: function(xhr) {
                    alert("Item deleted successfully");
                    window.location.href = "/list";
                },
                404: function(xhr) {
                    alert("Item ID not found");
                },
            },
        });
    });
});
