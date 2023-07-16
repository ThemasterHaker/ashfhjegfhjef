function renderChatMessages(data) {
    $('#chatbox').empty();
    data.reverse().forEach(function (msg) {
        $('#chatbox').append('<p><b>' + msg.username + ': </b>' + msg.msg + '</p>');
    });
}

function submitMessage() {
    const username = $('#chat-username').val();
    const message = $('#usermsg').val();

    $.ajax({
        type: "POST",
        url: '/chat-log',
        data: {username: username, usermsg: message},
        success: function (data) {
            renderChatMessages(data);
            $('#usermsg').val('');
        }
    });
}


$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: '/chat-log',
        success: renderChatMessages
    });
});
