function sendRequest(type, url, data) {
    $.ajax({
        type: type,
        url: url,
        dataType: "json",
        data: data,
        success: function(response) {
            handleResponse(response);
        },
    });
}

function getRequest(url, data) {
    sendRequest("GET", url, data);
}

function postRequest(url, data) {
    sendRequest("POST", url, data);
}

function putRequest(url, data) {
    sendRequest("PUT", url, data);
}

function deleteRequest(url, data) {
    sendRequest("DELETE", url, data);
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
    if (response) {
        if (response.errorMsg) {
            alertError(response.errorMsg);
        }
        redirect(response.redirectUrl);
    }
}
