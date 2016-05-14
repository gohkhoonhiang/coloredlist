$(document).ready(function() {
    $('#login-submit').click(function(e) {
        e.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        if (username && password) {
            var url = "/login/submit";
            var data = {"username":username, "password":password};
            postRequest(url, data);
        } else {
            alertError("Please enter both username and password");
        }
    });
});

