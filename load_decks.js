//1d_ao2_d10_s17_6rd_ra.json
//$.getJSON("./basic_strategy_6d_s17.json",function (data) {
$.getJSON("./6d_hilow_s17_75pen_ra.json",function (data) {
    console.log(data);
    $("#strategy_name").text(data.strategy);
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
}).fail(function () {
        console.log("not valid json???");
    });

function Strategy() {
}