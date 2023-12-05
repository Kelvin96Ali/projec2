document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  // Función para enviar el mensaje
  function sendMessage(message) {
    socket.emit("submit message", { message: message });
  }

  // Cuando se conecta con éxito al servidor WebSocket
  socket.on("connect", () => {
    // Configura un controlador de eventos para el evento 'keypress' en el elemento 'msg_box'
    document.getElementById("msg_box").addEventListener("keypress", (event) => {
      if (event.key === "Enter") {
        event.preventDefault(); // Evita el comportamiento predeterminado del Enter
        let message = event.target.value.trim(); // Obtiene el mensaje del cuadro de texto
        if (message !== "") {
          sendMessage(message); // Llama a la función para enviar el mensaje al servidor
          event.target.value = ""; // Limpia el contenido del cuadro de texto
        }
      }
    });

    // Configura un controlador de eventos para el clic en el elemento con el ID "send_message"
    document.getElementById("send_message").onclick = () => {
      let message = document.getElementById("msg_box").value.trim(); // Obtiene el mensaje del cuadro de texto
      if (message !== "") {
        sendMessage(message); // Llama a la función para enviar el mensaje al servidor
        document.getElementById("msg_box").value = ""; // Limpia el contenido del cuadro de texto
      }
    };
  });

  // Cuando el servidor envía un nuevo mensaje (evento "add messages")
  socket.on("add messages", (newMessage) => {
    const template = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${newMessage["author"]} says:</h5>
          ${newMessage["body"]}
        </div>
        <p class="card-text">
          <small class="text-muted">from ${newMessage["time_stamp"]}</small>
        </p>
      </div>
    `;
    document.getElementById("chat_area").innerHTML += template;
  });
});
