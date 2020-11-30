
class Socket {
  constructor(url, chat_manager) {
    this.ws = new WebSocket(url);
    this.ws.addEventListener('message', msg => this.handleMessage(msg));
    this.ws.addEventListener('close', function() {console.log("CLOSED")});

    this.chat_manager = chat_manager;
  }

  handleMessage(message) {
    let message_data = JSON.parse(message['data']);
    console.log("data: " + message.data);
    switch (message_data['type'])
    {
      case "chat_message":
        this.chat_manager.add_message(message_data['message'], message_data['player_name']);
        break;
      case "current_players":
        for (let i = 0; i < message_data['players'].length; i++) {
          console.log("player");
          let player = new Player(message_data['players'][i]['name'], 'green');
          add_player(player);
        }
        break;
      case "new_player":
        let player = new Player(message_data['player']['name'], 'green');
        add_player(player);
        break;
      case "player_left":
        remove_player(message_data['player_name']);
        break;
      case "start_game":
        let starter = document.getElementById("start_game");
        starter.click();
        break;
      case "owner_left":
        remove_player(message_data['player_name']);
        this.chat_manager.add_message("DER BESITZER HAT DEN RAUM VERLASSEN", "ACHTUNG!");
        break;
        //Hier sollte probably mehr passieren
      case "games":
        show_games(message_data['games'], this);
        break;
      case "game_set":
        let game_box = document.getElementById("game_header") || document.getElementById("game_owner_header");
        //if (game_box == null)
        //    game_box = document.getElementById("game_owner_header");
        game_box.innerHTML = message_data['game_name'];
        break;
    }
  }

  send_chat(message) {
    this.ws.send(JSON.stringify({'type':'message', 'message':message}));
  }

  start_game() {
    this.ws.send(JSON.stringify({'type':'start_game'}));
  }

  get_games() {
    this.ws.send(JSON.stringify({'type':'get_games'}));
  }

  set_game(game_name) {
    this.ws.send(JSON.stringify({'type':'set_game', 'game_name':game_name}));
  }

}
