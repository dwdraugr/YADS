function notification(type, message) {
    let container = document.getElementById('message_box');
    let message_box = document.createElement('div');
    message_box.className = "alert " + type;
    message_box.innerText = message;
    container.appendChild(message_box);
    window.scrollTo(0, 0);
    setTimeout(function () {
        message_box.remove();
    }, 3000)
}

