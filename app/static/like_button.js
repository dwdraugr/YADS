function like_button(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/test_like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            alert(request.responseText);
            btn = document.getElementById('like-' + uid);
            btn.className = 'btn btn-warning';
        }
    };
}

