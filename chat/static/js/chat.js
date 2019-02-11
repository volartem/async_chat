let CURRENT_CONNECTION = {};
let TOKEN = '';

$(function () {
    // get_weather().then(data => console.log(data), error => {console.log(error)});
    console.log("ready!");
    getMeassages();
});

function get_weather() {
    return new Promise((resolve, reject) => {
        $.get("/weather").then((data) => {
            let correctData = JSON.parse(data);
            resolve(correctData);
        }, error => {
            reject(error);
        });
    });
}

function getMeassages() {
    $(".chat-link").click(function () {
        let roomId = $(this).attr("href").replace("#", "");
        $(".friend-list").children().removeClass("active");
        $(this).parent().addClass("active");

        let room_url = "/messages/room/" + roomId;
        $.get(room_url).then(data => {
            displayMessages(data).then(() => {
                webSocketConnections(roomId);
            })
        }, error => {
            console.log(error)
        });
    })
}

function displayMessages(data) {
    return new Promise((resolve, reject) => {
        $("#chat").html("");
        $.each(data, function (count, item) {
            appendMessage(item.message_message, item.auth_user_username, item.message_created)
        });
        $("#chatMessages").animate({scrollTop: $("#chatMessages")[0].scrollHeight}, 5);
        resolve();
    });
}

function webSocketConnections(roomId) {
    console.log("roomId = " + roomId);

    if (!TOKEN) {
        getToken().then((token) => {
            websocketMessaging(token, roomId);
        }, error => {
            console.log(error)
        });
    } else {
        websocketMessaging(TOKEN, roomId);
    }
}

function websocketMessaging(token, roomId) {
    $("#chatBox").css("display", "block");
    let connection;
    TOKEN = token;
    let wsUrl = "ws://" + window.location.host + "/ws/" + roomId + "/?token=" + TOKEN;

    if (CURRENT_CONNECTION.url !== wsUrl) {
        if (CURRENT_CONNECTION && CURRENT_CONNECTION.url) {
            CURRENT_CONNECTION.close();
        }
        connection = getWebsocketConnection(wsUrl);
        console.log(connection.url);
        connection.onopen = function (event) {
            console.log("onopen");
        };
        connection.onclose = function (event) {
            console.log("onclose");
        };

        $('#sendMessage').off("click").on('click', function () {
            console.log("click on room id = " + roomId);
            let text = $("#inputMessageText").val();
            if (text) {
                connection.send(text);
            }
        });

        connection.onmessage = function (event) {
            console.log("on message");
            let data = JSON.parse(event.data);
            if (data.action !== 'error') {
                appendMessage(data.text, data.username, data.created);
                $("#chatMessages").animate({scrollTop: $('#chatMessages')[0].scrollHeight}, 'slow');
            } else {
                showError();
            }
        };

        CURRENT_CONNECTION = connection;
    }
}

function getToken() {
    return new Promise(function (resolve, reject) {
        $.get("/uuid/").then((data) => {
            console.log(data);
            resolve(data.token);
        }, error => {
            reject(error);
        });
    });
}


function getWebsocketConnection(wsUrl) {
    let connection;
    try {
        connection = new WebSocket(wsUrl);
    } catch (err) {
        connection = new WebSocket(wsUrl.replace("ws://", "wss://"));
    }
    return connection;
}

function appendMessage(text, user, created) {
    let chatDiv = $("#chat");
    let messageBlock = "<li class=\"left clearfix\">" +
        "   <span class=\"chat-img pull-left\">" +
        "   <img src=\"/static/images/cat_logo.png\" alt=\"User Avatar\">" +
        "   </span>" +
        "   <div class=\"chat-body clearfix\">" +
        "       <div class=\"header\">" +
        "           <strong class=\"primary-font\">" + user + "</strong>" +
        "           <small class=\"pull-right text-muted\"><i class=\"fa fa-clock-o\"></i>" + created + "</small>" +
        "       </div>" +
        "       <p>" + text + "</p>" +
        "   </div>" +
        "</li>";
    chatDiv.append(messageBlock);
}

function showError() {
    $("#errorWarningBlock").css("display", "block");
}