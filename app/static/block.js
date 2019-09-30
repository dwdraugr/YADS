window.onload = function () {
    let uids = document.getElementsByClassName('like-button');
    for (let i = 0; i < uids.length; i++) {
        like_get(uids[i].id.split('-')[1])
    }
    get_guests();
    get_likes();
    get_all_new_message();
    setInterval(function () {
        get_guests();
        get_likes();
        get_all_new_message();
    }, 10000);
};

function block(uid) {
    if (document.getElementById('block')
        .className === 'btn btn-warning') {
            block_user(uid);
        }
    else {
        ublock_user(uid);
    }
}

function block_user(uid) {
    let request = new XMLHttpRequest();
    request.open('PUT', '/api/v1.0/block/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            notification('alert-success', 'User add to blacklist!');
            let block_button = document.getElementById('block');
            block_button.className = 'btn btn-default';
            block_button.innerText = 'User blocked. Unblock?';
        }
    }
}

function check_block(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/block/' + uid);
    request.send();
    let block_button = document.getElementById('block');
    request.onreadystatechange = function () {
        if (request.status === 200) {
            block_button.className = 'btn btn-default';
            block_button.innerText = 'User blocked. Unblock?';
        }
    }
}

function ublock_user(uid) {
    let request = new XMLHttpRequest();
    request.open('DELETE', '/api/v1.0/block/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 204 && request.readyState === 4) {
            notification('alert-success', 'USer delete from black');
            let block_button = document.getElementById('block');
            block_button.className = 'btn btn-warning';
            block_button.innerText = 'Block user';
        }
    }
}