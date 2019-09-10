window.onload = function () {
    let uids = document.getElementsByClassName('like-button');
    for (let i = 0; i < uids.length; i++) {
        like_check(uids[i].id.split('-')[1])
    }
};

function like_button(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/test_like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            alert(request.responseText);
            let btn = document.getElementById('like-' + uid);
            btn.className = 'btn btn-warning';
        }
    };
}

function like_check(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
            let btn = document.getElementById('like-' + uid);
            btn.className = 'btn btn-warning'
        }
        else if (request.readyState === 4 && request.status === 404) {
            return 0;
        }
    }
}
