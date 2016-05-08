$(document).ready(function() {
    $('#new-account-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm-password').val();
        if (username && password && confirm_password) {
            if (password === confirm_password) {
                $.ajax({
                    type: "POST",
                    url: "/account/create/submit",
                    dataType: "json",
                    data: {"username": username, "password": password},
                    success: function(response) {
                        if (response) {
                            if (response.status != 201 && response.errorMsg) {
                                alert(response.errorMsg || "Failed to create account");
                            }
                            if (response.redirectUrl) {
                                window.location.href = response.redirectUrl;
                            }
                        }
                    },
                });
            } else {
                alert("Password and Confirm Password do not match!");
            }
        } else {
            alert("Username, password and confirm password should not be empty");
        }
    });
});
