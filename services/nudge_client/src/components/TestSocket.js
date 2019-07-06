import React from 'react';

class TestSocket extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      count: 90
    };
  }



  async startWebSocket () {
    console.log("Calling start ws");
    console.log('Sanity check')
    if ("WebSocket" in window) {
       console.log("WebSocket is supported by your Browser!");

       // Let us open a web socket
       var ws = new WebSocket("ws://localhost:5000");

       ws.onopen = function() {

          // Web Socket is connected, send data using send()
          ws.send("Message to send");
          console.log("Message is sent...");
       };

       ws.onmessage = function (evt) {
          console.log("Message is received...", evt);
       };

    } else {

       // The browser doesn't support WebSocket
       console.log("WebSocket NOT supported by your Browser!");
    }
  }

  render() {
    return (
      <div>
        <h1>Testing Redux</h1>
        <h5>Count: <strong>{this.state.count}</strong></h5>
        <button onClick={()=> this.startWebSocket()}>Start WS</button>
      </div>
    );
  }
}

export default TestSocket;