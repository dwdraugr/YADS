function delete_photo() {
    let phids = document.getElementsByClassName('active');
    if (phids === undefined)
        return 0;
    phid = phids[0].id;
    let request = new XMLHttpRequest();
    request.open('DELETE', '/api/v1.0/photo/' + phid + '/');
    request.send();
    request.onreadystatechange = function () {
        if (request.status === 204 && request.readyState === 4) {
            notification('alert-success', 'Photo was deleted!');
            setTimeout(function () {
                location.reload();
            }, 1500);
        }
    }
}