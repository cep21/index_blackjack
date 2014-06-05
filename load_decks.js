$.getJSON("./basic_strategy_6d_s17.json",function (data) {
    console.log(data);
    $("#strategy_name").text(data.strategy);
    $("#number_of_decks").text(data.decks);
    $("#double_after_split").text(data.DaS ? "Yes" : "No");
    $("#surrender").text(data.surrender);
    $("#hit_soft_17").text(data.hit_soft_17 ? "Yes" : "No");
    var hard_table = $("#hard_table")
    hard_table.empty();
    var head = $('<tr><td></td></tr>');
    for (i = 2; i < 11; i++) {
        head.append("<td>" + i + "</td>");
    }
    head.append("<td>A</td>");
    hard_table.append(head);

    for (i = 12; i < 22; i++) {
        head = $("<tr><td>" + i + "</td></tr>");
        for (j = 0; j < 10; j++) {
            head.append("<td>" + data.hard[i - 12][j] + "</td>");
        }
        hard_table.append(head);
    }

    var soft_table = $("soft_table")
    soft_table.empty();

}).fail(function () {
        console.log("not valid json???");
    });

function Strategy() {
}