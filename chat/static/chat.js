$(function () {
    console.log("ready!");
    getMeassages();
});

function getMeassages() {
    $(".chat-link").click(function () {
        console.log(this);

        let room_url = "/messages/room/" + $(this).attr("href").replace("#", "");
        $.get(room_url).then(data => {
            displayMessages(data)
        }, error => {
            console.log(error)
        });
    })
}

function displayMessages(data) {
    let chatDiv = $("#chat");
    chatDiv.html("");
    $.each(data, function (count, item) {
        let messageBlock = "<li class=\"left clearfix\">\n" +
            "                            <span class=\"chat-img pull-left\">\n" +
            "                                <img src=\"/static/cat_logo.png\" alt=\"User Avatar\">\n" +
            "                            </span>\n" +
            "                            <div class=\"chat-body clearfix\">\n" +
            "                                <div class=\"header\">\n" +
            "                                    <strong class=\"primary-font\">" + item.auth_user_username + "</strong>\n" +
            "                                    <small class=\"pull-right text-muted\"><i class=\"fa fa-clock-o\"></i>" + item.message_created + "</small>\n" +
            "                                </div>\n" +
            "                                <p>\n" + item.message_message + "</p>\n" +
            "                            </div>\n" +
            "                        </li>";
        chatDiv.append(messageBlock);
    });
}