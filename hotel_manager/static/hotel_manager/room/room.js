window.addEventListener("load", function() {
  let chat_table = document.getElementById("chat_table");
  var chat_manager = new ChatManager(chat_table);
  let room_nr = window.location.pathname.split('/')[window.location.pathname.split('/').length - 1];
  var sock = new Socket('ws://' + window.location.host + '/room/' + room_nr, chat_manager);
  let chat_input = document.getElementById("chat_input");
  chat_input.addEventListener('keydown', function(event) {
    if (event.keyCode == 13) {
      sock.send_chat(this.value);
      this.value = "";
    }
  });
  let start_button = document.getElementById("start_button");
  if (start_button != null)
  {
    start_button.addEventListener("click", function() {
      sock.start_game();
    });
  }

  let game_owner_header = document.getElementById("game_owner_header");
  if (game_owner_header != null)
  {
    game_owner_header.addEventListener("click", function() {
      sock.get_games();
    });
  }

});

function show_games(games, socket)
{
  let game_overlay = document.getElementById("game_overlay");
  if (game_overlay == null)
      return;

  let current_nodes = Array.from(game_overlay.childNodes);
  for (let i = 0; i < current_nodes.length; i++) {
    game_overlay.removeChild(current_nodes[i]);
  }

  for (let i = 0; i < games.length; i++) {
    let picker_node = document.createElement("div");
    picker_node.classList.add("game_picker");
    picker_node.style.top = i * picker_node.style.offsetHeight;
    picker_node.innerHTML = games[i];
    game_overlay.appendChild(picker_node);
    picker_node.addEventListener("click", function() {
      game_overlay.style.display = "none";
      let game_box = document.getElementById("game_owner_header");
      game_box.innerHTML = this.innerHTML;
      socket.set_game(this.innerHTML);
    });
  }

  // dann neue childs erstellen, die dann an das Socket schreiben, wenn geclickt wurde
  // dann closen wenn auf eines geclickt wurde

  game_overlay.style.display = "block";
}
