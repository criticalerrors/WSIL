/**
 * Created by ddipa on 15/06/2017.
 */

function getPlot(lang, id, type, url) {
    fetch(url + '?format=json')
        .then(function(data) {
            return data.json();
        })
        .then(function(json) {
            if (json.length == 0) {
                document.getElementById(id).innerHTML = "<h1>No data available</h1>";
                return;
            }
            var x = [];
            var y = [];
            for(var i = 0; i < json.length; i++) {
                x[i] = json[i]['date'];
                y[i] = json[i]['interest_rate'];
            }
            var data = [
                {
                    x: x,
                    y: y,
                    type: type
                }
            ];
            Plotly.newPlot(id, data);
        })
        .catch(function (error) {
            console.log(error);
        });
}