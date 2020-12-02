

window.addEventListener('load', function() {
  let room_nr = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
  var sock = new Socket('ws://' + window.location.host + '/werewolf/forest/' + room_nr);

  let settings_list = document.getElementsByClassName("setting_value");

  for (let i = 0; i < settings_list.length; i++) {
    settings_list[i].addEventListener('input', function() {
      sock.set_setting(settings_list[i].name, settings_list[i].value);
    });
  }
  let start_button = document.getElementById("start_button");
  if (start_button != null){
    start_button.addEventListener('click', function() {sock.start_game();});
  }


});
