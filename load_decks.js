$.getJSON("http://localhost/index_blackjack/basic_strategy_6d_s17.json", function( data ) {
  console.log(data);
  $("#number_of_decks").text(data.decks);
}).fail(function(){
  console.log("not valid json???");
});

function Strategy() {
}
