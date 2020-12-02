
class Socket {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.ws.addEventListener('message', msg => this.handleMessage(msg));
    this.ws.addEventListener('close', function() {console.log('close');});
  }

  handleMessage(msg)
  {
    let message_data = JSON.parse(msg['data']);
    console.log("data: " + msg.data);
    switch (message_data['type'])
    {
      case "players":
        for (let i = 0; i < message_data['players'].length; i++) {
          console.log("player");
          let player = new Player(message_data['players'][i]['name'], 'green');
          add_player(player);
        }
        break;
      case "setting_changed":
        let setting_value = document.getElementById(message_data['name'] + "_setting");
        setting_value.value = message_data['value'];
        break;
      case "start_game":
        let submit = document.getElementById("submit");
        submit.click();
        break;
    }
  }

  set_setting(name, value) {
    this.ws.send(JSON.stringify({
      'type':'set_setting',
      'name':name,
      'value':value
    }));
  }

  start_game() {
    this.ws.send(JSON.stringify({
      'type':'start_game'
    }));
  }
}
