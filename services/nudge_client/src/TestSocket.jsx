import React from 'react';

class TestSocket extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      count: 90
    };
  }

  async componentDidMount() {
    var response = await fetch("http://localhost:9000/");
    var body = await response.json();
    console.log("What is body: ", body)
    var es = new EventSource('http://localhost:9000/sse');
    es.onmessage = event => {
      console.log("What is ES event? ", event)
    }
  }

  async initWebSocket() {
    console.log("Initing ws")
    this.ws.onopen = event => {
      console.log("Open WS")
      this.ws.send("test")
    }
    this.ws.onmessage = event => {
      console.log("Message WS")
      console.log("What is data: ", event)
    }
  }

  async startWebSocket() {
    console.log("Calling start ws")
    const faust_ws = new WebSocket('ws://localhost:9000/ws/start')
    faust_ws.onopen = event => {
      console.log("Faust WS open")
    }
  }


  render() {
    return (
      <div>
        <h1>Halasdfsddo</h1>
        Count: <strong>{this.state.count}</strong>
        <button onClick={()=> this.startWebSocket()}>Start WS</button>
      </div>
    );
  }
}

export default TestSocket;