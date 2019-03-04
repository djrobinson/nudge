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
    this.ws = new WebSocket('ws://localhost:9000/ws')
    this.initWebSocket()
  }

  initWebSocket() {
    this.ws.onopen = event => {
      console.log("Open WS")
      this.ws.send("test")
    }
    this.ws.onmessage = event => {
      console.log("Message WS")
      let data = JSON.parse(event.data)
      console.log("What is data: ", data)
    }
  }


  render() {
    return (
      <div>
        <h1>Halasdfsddo</h1>
        Count: <strong>{this.state.count}</strong>
      </div>
    );
  }
}

export default TestSocket;