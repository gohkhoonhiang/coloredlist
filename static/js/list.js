$(document).ready(function() {
    $('#new-item-submit').click(function(e) {
        e.preventDefault();
        var text = $('#new-list-item-text').val();
        if (text) {
            var url = "/list/create";
            $.ajax({
                type: "POST",
                url: url,
                dataType: "json",
                data: {"text": text},
                success: function(response) {
                    if (response) {
                        if (response.status != 201 && response.errorMsg) {
                            alert(response.errorMsg || "Create item failed");
                        }
                        if (response.redirectUrl) {
                            window.location.href = response.redirectUrl;
                        }
                    }
                },
            });
        } else {
            alert("Item text should not be empty.");
        }
    });
    $('.edit-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var text = $(itemSpan).find("input[name='text']").val();
        if (text) {
            var url = "/list/" + itemId + "/edit";
            $.ajax({
                type: "PUT",
                url: url,
                dataType: "json",
                data: {"text": text},
                success: function(response) {
                    if (response) {
                        if (response.status != 200 && response.errorMsg) {
                            alert(response.errorMsg || "Update item failed");
                        }
                        if (response.redirectUrl) {
                            window.location.href = response.redirectUrl;
                        }
                    }
                },
            });
        } else {
            alert("Item text should not be empty.");
        }
    });
    $('.delete-button').click(function() {
        var itemSpan = $(this).parent();
        var itemId = $(itemSpan).find("input[type='hidden']").val();
        var url = "/list/" + itemId + "/delete";
        $.ajax({
            type: "DELETE",
            url: url,
            dataType: "json",
            data: {},
            success: function(response) {
                if (response) {
                    if (response.status != 200 && response.errorMsg) {
                        alert(response.errorMsg || "Delete item failed");
                    }
                    if (response.redirectUrl) {
                        window.location.href = response.redirectUrl;
                    }
                }
            },
        });
    });
});
