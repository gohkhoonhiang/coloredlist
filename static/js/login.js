$(document).ready(function() {
    $('#login-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        if (username && password) {
            $.ajax({
                type: "POST",
                url: "/login/submit",
                dataType: "json",
                data: {"username":username, "password":password},
                success: function(response) {
                    if (response) {
                        if (response.status != 200 && response.errorMsg) {
                            alert(response.errorMsg || "Unable to login");
                        }
                        if (response.redirectUrl) {
                            window.location.href = response.redirectUrl;
                        }
                    }
                },
            });
        } else {
            alert("Please enter both username and password");
        }
    });
});

