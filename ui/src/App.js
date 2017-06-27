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
                onClick={this.props.onClick}>
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
        /* this.props.config.plotOptions.series.point.events.drop = this.handleDrop.bind(this)        */
        this.state = {points: Object.assign({}, this.props.config.series[0].data)}
    }
    /* 
     *     handleDrop(e) {
     *         console.log('heyo')
     *         console.log(e)
     *         console.log(this.chart)
     *         console.log(this.state.points)
     *     }*/

    afterRender(chart) {
        console.log(chart)
        this.chart = chart
        /* chart.options.plotOptions.series.point.events.drag = function(e) {
         *     console.log('it works')
         * }
         * console.log(chart.options.plotOptions)*/
    }

    /* chartCallback(chart) {
     *     console.log(chart)
     *     console.log(chart.props.config.plotOptions.series.point.events.drag)

     *     chart.props.config.plotOptions.series.point.events.drag = function(e) {
     *         console.log('it works')
     *     }
     *     this.chart = chart
     * }*/
    
    render() {
        // TODO: Get DOM changes into state
        return (
            <ReactHighCharts config={this.props.config}
                             callback={this.afterRender}

            >
            </ReactHighCharts>
        )        
    }
}

class ChartFormContainer extends Component {
    constructor(props) {
        super(props)
        this.state = {chart: {points: this.props.chartConfig.series[0].data}}
    }

    handleSubmit(e) {
        console.log(this.state)
    }
    
    render() {
        console.log(this.state)
        return (
            <div>
                <EditableChart config={this.props.chartConfig}></EditableChart>
                <SubmitButton label="Make playlist" onClick={this.handleSubmit.bind(this)}>
                </SubmitButton>
            </div>
            
        )
    }
}

/* ref={(chart) => this.chartCallback(chart)}*/


class App extends Component {
  render() {
    return (
        <div className="App">
            <ChartFormContainer chartConfig={chartConfig}></ChartFormContainer>
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
