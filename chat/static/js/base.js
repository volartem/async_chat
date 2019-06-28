
$(function () {
    get_data("/weather").then(data => {
        $('#weatherTemp').html(data.main.temp);
        $('#weatherHum').html(data.main.humidity);
        $('#weatherCloud').html(data.weather[0].description);
        $("#weatherDiv").css("display", "table-cell");
    }, error => {
        console.log(error)
    });
    get_data("/currencies").then(data => {
        for(let i in data){
           setCurrentCurrency(data,data[i]);
        }
        $("#currencyDiv").css("display", "table-cell");
    }, error => {
        console.log(error);
    });

    console.log("base ready!");
});

function setCurrentCurrency(data, currency) {
    $("#" + currency.ccy.toLowerCase() + "Currency").html(" " + currency.buy + " / " + currency.sale);
}

function get_data(url) {
    return new Promise((resolve, reject) => {
        $.get(url).then((data) => {
            let correctData = JSON.parse(data);
            resolve(correctData);
        }, error => {
            reject(error);
        });
    });
}
