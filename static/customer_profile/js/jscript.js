function edit_mode_on() {

    $('#edit').css('display', 'none');
    $('#delete').css('display', 'none');
    $('h2').css('display', 'none');
    $('#profileImage').css('display', 'none');
    $('.profile-img h3').css('display', 'none');

    $('#uploadImage').css('display', 'block');
    $('#details :input').css('display', 'block');
    $('select').css('display', 'block');
    $('#save').css('display', 'block');

}

