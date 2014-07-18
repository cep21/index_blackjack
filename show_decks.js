function add_chart_row(chart_name) {
    $.getJSON('json/' + chart_name + ".json",function (data) {
        console.log(data);
        var row = $('<tr class="show_row"></tr>');
        row.append($('<td class="show_data">' + data.strategy + '</td>'));
        row.append($('<td class="show_data">' + data.decks + '</td>'));
        row.append($('<td class="show_data">' + (data.DaS ? "Yes" : "No") + '</td>'));
        row.append($('<td class="show_data">' + (data.hit_soft_17 ? "Yes" : "No") + '</td>'));
        row.append($('<td class="show_data">' + data.surrender_allowed + '</td>'));
        row.append($('<td class="show_data">' + data.counting_method + '</td>'));
        row.append($('<td class="show_data">' + (data.extra ) + '</td>'));
        row.append($('<td class="show_data"><a href=./show_chart.html?chart=' + chart_name +'>See chart</a></td>'));
        $('#chart_link_table').append(row);
    }).fail(function () {
            console.log("not valid json???");
        });
}
