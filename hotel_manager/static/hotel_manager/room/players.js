var player_array_left = [];
var player_array_right = [];

const player_avatar_offset = 111;
const player_name_offset = 97;
const player_name_template = document.getElementById("player_name_1");
const player_avatar_template = document.getElementById("player1_symbol");
const player_container_right = document.getElementById("player_container_right");
const player_container_left = document.getElementById("player_container_left");

class Player
{
  constructor(name, color) {
    this.name = name;
    this.color = color;
    //this.avatar =
  }
}
// vlt in die Player Class hauen

function add_player(player)
{
  if (player_array_left.length + 1 < 6) {
    player_array_left.push(player)
    var length = player_array_left.length;
    var container = player_container_left;
  } else {
    player_array_right.push(player)
    var length = player_array_right.length;
    var container = player_container_right;
  }
  let player_avatar = player_avatar_template.cloneNode();
  player_avatar.id = player.name + "_avatar";
  player_avatar.style.display = "block";
  player_avatar.style.transform = "translateY(" + player_avatar_offset * (length-1) + "px)";
  container.appendChild(player_avatar);

  let player_name = player_name_template.cloneNode();
  player_name.id = player.name + "_name";
  player_name.style.display = "block";
  player_name.style.transform = "translateY(" + (length != 1 ? player_avatar_offset * length - 28 : 83) + "px)";
  player_name.style.backgroundColor = player.color;
  player_name.innerHTML = player.name;
  container.appendChild(player_name);
}

function remove_player(player_name)
{
  let player = null;
  let new_player_array = [];
  for (let i = 0; i < player_array_left.length; i++)
  {
    if (player_array_left[i].name == player_name) {
      player = player_array_left[i];
      player_array_left.splice(i, 1);
      break;
    }
  }
  for (let i = 0; i < player_array_right.length; i++)
  {
    if (player_array_right[i].name == player_name) {
      player = player_array_right[i];
      player_array_right.splice(i, 1);
      break;
    }
  }
  new_player_array = player_array_left.concat(player_array_right);

  let left_childs = Array.from(player_container_left.childNodes);
  for (let i = 0; i < left_childs.length; i++) {
    player_container_left.removeChild(left_childs[i]);
  }
  let right_childs = Array.from(player_container_right.childNodes);
  for (let i = 0; i < right_childs.length; i++) {
    player_container_right.removeChild(right_childs[i]);
  }
  player_array_left = [];
  player_array_right = [];

  for (let i = 0; i < new_player_array.length; i++) {
    add_player(new_player_array[i]);
  }
}
