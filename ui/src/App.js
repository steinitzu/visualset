import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import HighCharts from 'highcharts'
import makeDraggable from 'highcharts-draggable-points'
import ReactHighCharts from 'react-highcharts'
import chartConfig from './ChartConfig'


// monkey patching or something
makeDraggable(HighCharts)


class SubmitButton extends Component {
    render() {
        return (
            <button
                type="button"
                onClick={this.props.actions.onClick}>
                {this.props.label}
            </button>
        )
    }
}


class LoadingSpinner extends Component {
    render() {
        return (
            <i className="fa fa-spinner fa-spin fa-2x" aria-hidden="true"></i>
        )
    }
}


class PlaylistResult extends Component {
    render() {
        return (
            <a href={this.props.Url} target="_blank">
                Your playlist is ready
            </a>
        )
    }
}


class EditableChart extends Component {

    constructor(props) {
        super(props)
        this.state = {points: Object.assign({}, this.props.config.series[0].data)}
    }
    
    render() {
        // TODO: Get DOM changes into state
        return (
            <ReactHighCharts config={this.props.config}>                
            </ReactHighCharts>
        )        
    }
}



class App extends Component {
  render() {
    return (
        <div className="App">
            <EditableChart config={chartConfig}></EditableChart>
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;
