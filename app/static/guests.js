function check_guests() {
    let request = new XMLHttpRequest;
    request.open('POST', '/api/v1.0/guest/');
    request.send();
    request.onreadystatechange = function () {
        if (!(request.status === 200)) {
            alert('biba');
        }
    }
}

function get_guests() {
    let request = new XMLHttpRequest;

    request.open('GET', '/api/v1.0/guest/');
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let result = JSON.parse(request.responseText)['a'];
            document.getElementById('guest_num')
                .innerText = result.length;
            document.getElementById('modal-body').innerText = result.toString();
        }
        else {
            document.getElementById('guest_num')
                .innerText = 'bibos';
        }
    }
}