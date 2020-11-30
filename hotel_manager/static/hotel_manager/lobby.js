var join_button = document.getElementById("join_button");

var name_input = document.getElementById("name_input");

var submit_name = document.getElementById("submit_name");
var submit_avatar = document.getElementById("submit_avatar");
var submit = document.getElementById("submit");




join_button.addEventListener("click", function() {
  submit_name.value = name_input.value;
  submit_avatar.value = "0";
  submit.click();
});
