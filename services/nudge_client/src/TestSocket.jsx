import React from 'react';

class TestSocket extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      count: 90
    };
  }

  async componentDidMount() {
    var response = await fetch("http://localhost:6066/test");
    var body = await response.text();
    console.log("What is body: ", body)
    var es = new EventSource('http://localhost:6066/sse');
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
    var response = await fetch("http://localhost:6066/ws/start");
    var body = await response.json();
    console.log("What is start ws: ", body)
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