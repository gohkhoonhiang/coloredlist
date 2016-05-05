$(document).ready(function() {
    $('#logout-btn').click(function() {
        $.ajax({
            type: "POST",
            url: "/logout",
            success: function(response) {
                if (response) {
                    response = JSON.parse(response);
                    if (response.status == 200) {
                        alert(response.errorMsg || "Logged out successfully.");
                    } else {
                        alert(response.errorMsg || "Error logging out");
                    }
                    window.location.href = response.redirectUrl;
                }
            }
        });
    }); 
});
