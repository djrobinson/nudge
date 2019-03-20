import React, { Component } from 'react'
import { connect } from 'react-redux'
import TestSocket from './components/TestSocket'
import { simpleAction } from './actions/actions'
import './App.css';
class App extends Component {

    simpleAction = (event) => {
     this.props.simpleAction();
    }
 render() {
  return (
   <div className="App">
    <header className="App-header">
      <h1>Nudge</h1>
        <button onClick={this.simpleAction}>Test action</button>
        <pre>
         {
          JSON.stringify(this.props)
         }
        </pre>
    </header>
    <TestSocket />
  </div>
  )
 }
}

const mapStateToProps = state => ({
 ...state
})

const mapDispatchToProps = dispatch => ({
 simpleAction: () => dispatch(simpleAction())
})

export default connect(mapStateToProps, mapDispatchToProps)(App)