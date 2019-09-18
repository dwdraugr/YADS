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
            let result = JSON.parse(request.responseText)['guests'];
            document.getElementById('guest_num')
                .innerText = result.length;
            fill_window(result)
        }
        else {
            return 0;
        }
    }
}

function fill_window(users) {
    JSON.stringify(users);
    let list = document.createElement('li');
    list.className = 'list-group';
    let modal_body = document.getElementsByClassName('modal-body')[0];
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
        first_last_names.style.whiteSpace = 'nowrap';
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