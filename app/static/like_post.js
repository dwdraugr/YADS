window.onload = function () {
    let uids = document.getElementsByClassName('like-button');
    for (let i = 0; i < uids.length; i++) {
        like_get(uids[i].id.split('-')[1])
    }
    uids = document.getElementsByClassName('last-message');
    for (let i = 0; i < uids.length; i++){
        get_last_message(uids[i].id.split('-')[1]);
        get_messages_num(uids[i].id.split('-')[1]);
    }

    let objDiv = document.getElementById("scroll");
    if (objDiv) {
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    get_guests();
    get_likes();
    get_all_new_message();
    setInterval(function () {
        get_guests();
        get_likes();
        get_all_new_message();
        get_all_new_message();
    }, 10000);
};

function like(uid) {
    let btn = document.getElementById('like-' + uid);
    if (btn.className === 'like-button btn btn-primary')
        like_post(uid);
    else
        like_del(uid)
}

function like_post(uid) {
    let request = new XMLHttpRequest();
    request.open('POST', '/api/v1.0/like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 201) {
            let btn = document.getElementById('like-' + uid);
            btn.className = 'like-button btn btn-warning';
        }
        else  {
            notification('alert-info','Oh my lovely narcissist 😘');
            request.onreadystatechange = null;
        }
    };
}

function like_get(uid) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200) {
            let btn = document.getElementById('like-' + uid);
            btn.className = 'like-button btn btn-warning'
        }
        else if (request.readyState === 4 && request.status === 404) {
            return 0;
        }
    }
}

function like_del(uid) {
    let request = new XMLHttpRequest();
    request.open('DELETE', '/api/v1.0/like/' + uid);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200) {
            let btn = document.getElementById('like-' + uid);
            btn.className = 'like-button btn btn-primary';
        }
        else {
            notification('alert-danger','Ты чэ дурак? Удаляет неудаляемое он. Пидр');
            request.onreadystatechange = null;
        }
    }
}
