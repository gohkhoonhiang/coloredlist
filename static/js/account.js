$(document).ready(function() {
    $('#new-account-submit').click(function(e) {
        if ($('#password').val() === $('#confirm-password').val()) {
            $('#account-create-form').submit();
        } else {
            e.preventDefault();
            alert('Password and Confirm Password do not match!');
        }
    });
});
