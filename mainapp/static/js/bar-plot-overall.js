/**
 * Created by ddipa on 15/06/2017.
 */
function plot(url) {
    fetch(url + '?format=json')
        .then(function(data) {
            return data.json();
        })
        .then(function(json) {
            var x = [];
            var y = [];
            for(var i = 0; i < json.length; i++) {
                x[i] = json[i]['language'];
                y[i] = json[i]['repository_count'];
            }
            var data = [
                {
                    x: x,
                    y: y,
                    type: 'bar'
                }
            ];
            Plotly.newPlot('barPlot', data);
        })
        .catch(function (error) {
            console.log(error);
        });
}
