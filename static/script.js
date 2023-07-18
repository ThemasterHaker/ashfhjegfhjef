// REPLACED SOCKETIO LOGIC WITH AJAX REQUESTS, ALLOWS CHAT MSG TO SEND WITHOUT PAGE REFRESH

// RENDERS CHAT MESSAGES
function renderChatMessages(data) {
    $('#chatbox').empty();
    data.reverse().forEach(function (msg) {
        $('#chatbox').append('<p><b>' + msg.username + ': </b>' + msg.msg + '</p>');
    });
}

// LOGS MESSAGE TO DATABASE WHEN RECEIVED, IF SUCCESS, RENDER CHAT MESSAGES
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

// WAIT UNTIL PAGE IS LOADED, THEN RENDER CHAT MESSAGES
$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: '/chat-log',
        success: renderChatMessages
    });
});
