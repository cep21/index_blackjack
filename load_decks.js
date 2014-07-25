var QueryString = function () {
    // This function is anonymous, is executed immediately and
    // the return value is assigned to QueryString!
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        // If first entry with this name
        if (typeof query_string[pair[0]] === "undefined") {
            query_string[pair[0]] = pair[1];
            // If second entry with this name
        } else if (typeof query_string[pair[0]] === "string") {
            var arr = [ query_string[pair[0]], pair[1] ];
            query_string[pair[0]] = arr;
            // If third or later entry with this name
        } else {
            query_string[pair[0]].push(pair[1]);
        }
    }
    return query_string;
} ();


$.getJSON('json/' + QueryString.chart + ".json",function (data) {
    console.log(data);
    $("#strategy_name").text(data.strategy);
    $("#counting_method").text(data.counting_method);
    $("#extras").text(data.extra);
    $("#number_of_decks").text(data.decks);
    $("#double_after_split").text(data.DaS ? "Yes" : "No");
    $("#surrender_allowed").text(data.surrender_allowed);
    $("#hit_soft_17").text(data.hit_soft_17 ? "Yes" : "No");
    $("#insurance_index").text(data.insurance);
    var card_tables = [null, "A", "2", "3", "4", "5", "6", "7", "8", "9", "X", "A"];
    {
        var hard_table = $("#hard_table")
        hard_table.empty();
        hard_table.addClass("basic_table")
        var head = $('<tr class="head_row"><td class="head_data"></td></tr>');
        for (i = 2; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        hard_table.append(head);

        for (i = 12; i < 22; i++) {
            head = $("<tr><td>" + i + "</td></tr>");
            for (j = 0; j < 10; j++) {
                var td = $("<td>" + data.hard[i - 12][j] + "</td>");
                if (data.hard[i - 12][j] == "H") {
                    td.addClass('hit_data');
                }else if (data.hard[i - 12][j] == "S"){
                    td.addClass('stand_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            hard_table.append(head);
        }
    }

    {
        var soft_table = $("#soft_table")
        soft_table.empty();
        soft_table.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 2; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        soft_table.append(head);

        for (i = 2; i < 11; i++) {
            head = $("<tr><td> A/" + card_tables[i] + " (" + (11 + i) + ")</td></tr>");
            for (j = 0; j < 10; j++) {
                var td = $("<td>" + data.soft[i - 2][j] + "</td>");
                if (data.soft[i - 2][j] == "H") {
                    td.addClass('hit_data');
                }else if (data.soft[i - 2][j] == "S"){
                    td.addClass('stand_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            soft_table.append(head);
        }
    }
    {
        var hard_double = $("#hard_double_table")
        hard_double.empty();
        hard_double.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 2; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        hard_double.append(head);

        for (i = 5; i < 12; i++) {
            head = $("<tr><td>" + i + "</td></tr>");
            for (j = 0; j < 10; j++) {
                var td = $("<td>" + data.hard_double[i - 5][j] + "</td>")
                if (data.hard_double[i - 5][j] == "D") {
                    td.addClass('double_data');
                }else if (data.hard_double[i - 5][j] == "_"){
                    td.addClass('no_double_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            hard_double.append(head);
        }
    }

    {
        var soft_table = $("#soft_double_table")
        soft_table.empty();
        soft_table.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 2; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        soft_table.append(head);

        for (i = 2; i < 11; i++) {
            head = $("<tr><td> A/" + card_tables[i] + " (" + (11 + i) + ")</td></tr>");
            for (j = 0; j < 10; j++) {
                var td = $("<td>" + data.soft_double[i - 2][j] + "</td>")
                if (data.soft_double[i - 2][j] == "D") {
                    td.addClass('double_data');
                }else if (data.soft_double[i - 2][j] == "_"){
                    td.addClass('no_double_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            soft_table.append(head);
        }
    }

    {
        var soft_table = $("#split_table")
        soft_table.empty();
        soft_table.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 2; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        soft_table.append(head);

        for (i = 2; i < 12; i++) {
            head = $("<tr><td>" + card_tables[i] + "," + card_tables[i] + "</td></tr>");
            for (j = 0; j < 10; j++) {
                var td = $("<td>" + data.split[i - 2][j] + "</td>")
                if (data.split[i - 2][j] == "P") {
                    td.addClass('split_data');
                }else if (data.split[i - 2][j] == "_"){
                    td.addClass('no_split_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            soft_table.append(head);
        }
    }
    if (data.surrender_allowed == "None") {
        $("#surrender_hard_table").remove();
        $("#surrender_hard_table_header").remove();
        $("#surrender_split_table").remove();
        $("#surrender_split_table_header").remove();
        return;
    }
    {
        var table = $("#surrender_hard_table")
        table.empty();
        table.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 7; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        table.append(head);

        for (i = 12; i <= 17; i++) {
            head = $("<tr><td>" + i + "</td></tr>");
            for (j = 7; j < 12; j++) {
                var td = $("<td>" + data.surrender_hard[i - 12][j - 7] + "</td>")
                if (data.surrender_hard[i - 12][j - 7] == "R") {
                    td.addClass('surrender_data');
                }else if (data.surrender_hard[i - 12][j - 7] == "_"){
                    td.addClass('no_surrender_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            table.append(head);
        }
    }
    {
        var table = $("#surrender_split_table")
        table.empty();
        table.addClass("basic_table")
        head = $('<tr><td class="head_data"></td></tr>');
        for (i = 7; i < 12; i++) {
            head.append('<td class="head_data">' + card_tables[i] + "</td>");
        }
        table.append(head);

        for (i = 7; i <= 8; i++) {
            head = $("<tr><td>" + i + "</td></tr>");
            for (j = 7; j < 12; j++) {
                var td = $("<td>" + data.surrender_split[i - 7][j - 7] + "</td>")
                if (data.surrender_split[i - 7][j - 7] == "R") {
                    td.addClass('surrender_data');
                }else if (data.surrender_split[i - 7][j - 7] == "_"){
                    td.addClass('no_surrender_data');
                } else {
                    td.addClass('index_data');
                }
                head.append(td);
            }
            table.append(head);
        }
    }
}).fail(function () {
        console.log("not valid json???");
    });

function Strategy() {
}