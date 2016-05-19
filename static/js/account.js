$(document).ready(function() {
    $('#new-account-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm-password').val();
        if (username && password && confirm_password) {
            if (password === confirm_password) {
                var url = "/account/create/submit";
                var data = {"username":username, "password":password};
                postRequest(url, data, "/list", "/account/create");
            } else {
                alertError("Password and Confirm Password do not match!");
            }
        } else {
            alertError("Username, password and confirm password should not be empty");
        }
    });
});
