function get_online(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/online/' + uid);
    request.send();
    let online_status = document.getElementById('online-' + uid);
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let response = JSON.parse(request.responseText);
            if (response['online']  === 'Online') {
                online_status.innerText = '🌝 ' + response['online'];
            }
            else {
                online_status.innerText = '🌚, Last visit ' + response['online'];
            }
        }
        else {
            online_status.innerText = '🤔 ' + 'Not found';
        }
    }
}