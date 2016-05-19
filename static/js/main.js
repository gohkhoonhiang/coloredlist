$(document).ready(function() {
    $('#logout-btn').click(function(e) {
        e.preventDefault();
        var url = "/logout";
        var data = {};
        postRequest(url, data, "/login", "/login");
    }); 
});
