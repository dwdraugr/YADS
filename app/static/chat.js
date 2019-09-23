function get_new_message(you_id) {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/message/' + you_id);
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let data = JSON.parse(request.responseText);
            for (let i = 0; i < data['new_messages'].length; i++) {
                generate_your_message(data['new_messages'][i])
            }
        }
    }
}

function get_all_new_message() {
    let request = new XMLHttpRequest();
    request.open('GET', '/api/v1.0/message/');
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 200 && request.readyState === 4) {
            let data = JSON.parse(request.responseText);
            if (data['num_message'] !== 0)
                document.getElementById('message_num')
                    .innerText = data['num_message'];
            else {
                return 0
            }
        }
    }
}

function send_message(you_id) {
    let data = new FormData();
    data.append('message', document.getElementById('btn-input').value);
    let request = new XMLHttpRequest();
    request.open('POST', '/api/v1.0/message/' + you_id);
    request.send(data);
    request.onreadystatechange = function () {
        if (request.status === 201 && request.readyState === 4) {
            let resp = JSON.parse(request.responseText);
            generate_my_message({
                'sender': resp['id'],
                'receiver': you_id,
                'message_date': resp['message_date'],
                'text': document.getElementById('btn-input').value
            });
        }

    }
}

function generate_your_message(json_message) {
    let element = document.createElement('li');
    element.className = 'left clearfix';
    let span = document.createElement('span');
    let img = document.createElement('img');
    span.className = 'chat-img pull-left';
    img.src = document.getElementById(json_message['sender']).src;
    img.className = 'img-circle';
    img.style.width = '64px';
    img.style.height = '64px';
    span.appendChild(img);
    element.appendChild(span);

    let glyph = document.createElement('span');
    glyph.className = 'glyphicon glyphicon-time';
    let message_time = document.createElement('span');
    message_time.className = 'message-time';
    message_time.innerText = json_message['message_date'];
    let small = document.createElement('small');
    small.className = 'pull-right text-muted';
    small.appendChild(glyph);
    small.appendChild(message_time);
    let strong = document.createElement('strong');
    strong.className = 'primary-front';
    strong.innerText = document.getElementById(json_message['receiver']).className;
    let inner_div = document.createElement('div');
    inner_div.className = 'header';
    inner_div.appendChild(strong);
    inner_div.appendChild(small);
    let message = document.createElement('p');
    message.innerText = json_message['text'];
    let outer_div = document.createElement('div');
    outer_div.className = 'chat-body clearfix';
    outer_div.appendChild(inner_div);
    outer_div.appendChild(message);

    element.appendChild(outer_div);
    document.getElementById('chat').appendChild(element);
}

function generate_my_message(json_message) {
    let element = document.createElement('li');
    element.className = 'right clearfix';
    let span = document.createElement('span');
    let img = document.createElement('img');
    span.className = 'chat-img pull-right';
    img.src = document.getElementById(json_message['sender']).src;
    img.className = 'img-circle';
    img.style.width = '64px';
    img.style.height = '64px';
    span.appendChild(img);
    element.appendChild(span);

    let glyph = document.createElement('span');
    glyph.className = 'glyphicon glyphicon-time';
    let message_time = document.createElement('span');
    message_time.className = 'message-time';
    message_time.innerText = json_message['message_date'];
    let small = document.createElement('small');
    small.className = ' text-muted';
    small.appendChild(glyph);
    small.appendChild(message_time);
    let strong = document.createElement('strong');
    strong.className = 'pull-right primary-front';
    strong.innerText = document.getElementById(json_message['sender']).className;
    let inner_div = document.createElement('div');
    inner_div.className = 'header';
    inner_div.appendChild(small);
    inner_div.appendChild(strong);
    let message = document.createElement('p');
    message.innerText = json_message['text'];
    message.className = 'message-right';
    let outer_div = document.createElement('div');
    outer_div.className = 'chat-body clearfix';
    outer_div.appendChild(inner_div);
    outer_div.appendChild(message);

    element.appendChild(outer_div);
    document.getElementById('chat').appendChild(element);
}