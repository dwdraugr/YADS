function upload_image() {
    let input = document.getElementById('img');
    let form = new FormData();
    form.append('img', input.files[0]);

    let request = new XMLHttpRequest();
    request.open('POST', '/api/v1.0/photo/0/');
    request.send(form);
    request.onreadystatechange = function () {
        if (request.status === 201 && request.readyState === 4) {
            notification('alert-success', 'Image create success!');
            setTimeout(function () {
                location.reload()
            }, 3500);
        }
        else {
            console.log(request.status + ' ' + request.responseText);
        }
    }
}