
var dimmer_container = document.getElementById("dimmer_container");

var join_room = document.getElementById("join_room");
var create_room = document.getElementById("create_room");


var new_room_submit = document.getElementById("new_room_submit");
var join_room_submit = document.getElementById("join_room_submit");
var join_submit = document.getElementById("submit");



join_room.addEventListener("click", function() {
  dimmer_container.style.display = "block";
});

create_room.addEventListener("click", function() {
  new_room_submit.click();
});

join_submit.addEventListener("click", function() {
  if (document.getElementById("roomkey_input").value == "" && document.getElementById("roomnr_input").value == "")
      return;
  join_room_submit.click();
});
