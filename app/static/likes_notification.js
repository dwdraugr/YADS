function check_likes() {
    let request = new XMLHttpRequest;
    request.open('POST', '/api/v1.0/like/');
    request.send();
    request.onreadystatechange = function () {
        if (!(request.status === 200)) {
            alert('biba');
        }
        else
            location.reload();
    }
}

function get_likes() {
    let request = new XMLHttpRequest;

    request.open('GET', '/api/v1.0/like/');
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let result = JSON.parse(request.responseText)['likes'];
            document.getElementById('like_num')
                .innerText = result.length;
            fill_window_l(result)
        }
        else {
            return 0;
        }
    }
}

function fill_window_l(users) {
    JSON.stringify(users);
    let list = document.createElement('li');
    list.className = 'list-group';
    let modal_body = document.getElementsByClassName('modal-body')[1];
    modal_body.innerHTML = '';
    for (let i = 0; i < users.length; i++) {
        let img = document.createElement('img');
        img.src = '/api/v1.0/photo/' + users[i]['photos'][0] + '/';
        img.style.width = '64px';
        img.style.height = '64px';
        img.style.objectFit = 'cover';
        img.style.marginTop = '0.5em';

        let paragraph = document.createElement('span');
        paragraph.innerText = users[i]['first_name'] + ' ' + users[i]['last_name'];
        paragraph.style.marginLeft = '1em';

        let first_last_names = document.createElement('a');
        // first_last_names.style.whiteSpace = 'nowrap';
        first_last_names.href = '/user/' + users[i]['id'];
        first_last_names.appendChild(img);
        first_last_names.appendChild(paragraph);

        let list_element = document.createElement('ul');
        list_element.className = 'list-grout-item';
        list_element.appendChild(first_last_names);
        list.appendChild(list_element);
    }
    modal_body.appendChild(list);
}