$(document).ready(function() {
    $('#logout-btn').click(function() {
        $.ajax({
            type: "POST",
            url: "/logout",
            dataType: "json",
            data: {},
            success: function(response) {
                if (response) {
                    if (response.status != 200 && response.errorMsg) {
                        alert(response.errorMsg || "Error logging out");
                    }
                    if (response.redirectUrl) {
                        window.location.href = response.redirectUrl;
                    }
                }
            },
        });
    }); 
});
