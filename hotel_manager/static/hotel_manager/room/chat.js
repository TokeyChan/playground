

class ChatManager {
  constructor(chat_table) {
    this.table = chat_table;
    this.chat_messages = [];
  }
  add_message(message, player_name) {
    let row = this.table.insertRow(0);
    let cell = row.insertCell(0);
    cell.innerHTML = player_name + ": " + message;

  }
}
