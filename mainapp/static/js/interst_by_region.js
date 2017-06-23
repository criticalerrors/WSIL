/**
 * Created by ddipa on 23/06/2017.
 */

function plotRegion(url, title, myDiv) {

    Plotly.d3.json(url + "?format=json", function(err, rows){

        function unpack(rows, key) {
            return rows.map(function(row) {
                return row[key] });
        }

        var data = [{
            type: 'choropleth',
            locationmode: 'country names',
            locations: unpack(rows, 'region'),
            z: unpack(rows, 'interest_rate'),
            text: unpack(rows, 'region'),
            autocolorscale: true
        }];

        var layout = {
            title: title,
            geo: {
                projection: {
                    type: 'robinson'
                }
            }
        };

        Plotly.plot(myDiv, data, layout, {showLink: false});

    });

}