function sendRequest(type, url, data, successUrl, errorUrl) {
    $.ajax({
        type: type,
        url: url,
        dataType: "json",
        data: data,
        success: function(response) {
            handleResponse(response);
            redirect(successUrl);
        },
        error: function(response) {
            handleResponse(response);
            if (response.status == 403) {
                redirect("/login");
            } else {
                redirect(errorUrl);
            }
        },
    });
}

function getRequest(url, data, successUrl, errorUrl) {
    sendRequest("GET", url, data, successUrl, errorUrl);
}

function postRequest(url, data, successUrl, errorUrl) {
    sendRequest("POST", url, data, successUrl, errorUrl);
}

function putRequest(url, data, successUrl, errorUrl) {
    sendRequest("PUT", url, data, successUrl, errorUrl);
}

function deleteRequest(url, data, successUrl, errorUrl) {
    sendRequest("DELETE", url, data, successUrl, errorUrl);
}

function redirect(url) {
    if (url) {
        window.location.href = url;
    }
}

function alertError(errorMsg) {
    alert(errorMsg || "An error has occurred");
}

function handleResponse(response) {
    if (response && response.responseJSON) {
        if (response.responseJSON.errorMsg) {
            alertError(response.responseJSON.errorMsg);
        }
    }
}
