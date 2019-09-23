function get_last_message(you_id) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/last_message/' + you_id);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let data = JSON.parse(request.responseText);
            document.getElementById("message-" + you_id).innerText=data['new_messages']['text'];
        }
    }
}

function get_messages_num(you_id) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/message_non_check/' + you_id);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let data = JSON.parse(request.responseText);
            let badge = document.getElementById("badge-" + you_id);
            badge.innerText=data['new_messages'].length;
            badge.style.display = 'inline-block';
        }
    }
}