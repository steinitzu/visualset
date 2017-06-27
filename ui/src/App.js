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
                onClick={this.props.onClick}
                disabled={this.props.disabled}>
                {this.props.label}
            </button>
        )
    }
}


class LoadingSpinner extends Component {
    render() {
        return (
            <div>
                <span>Building your playlist</span>
                <i className="fa fa-spinner fa-spin fa-2x" aria-hidden="true"></i>
            </div>
        )
    }
}


class PlaylistResult extends Component {
    render() {
        return (
            <a href={this.props.url} target="_blank">
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

    afterRender(chart) {
        this.chart = chart
    }

    
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
        this.state = {
            chart: {points: this.props.chartConfig.series[0].data},
            submitLoading: false,
            playlistUrl: null
        }
    }

    loginCallback(e) {
        // TODO: react send some message event to window which breaks JSON parsing        
        console.log(e)
        let data = JSON.parse(e.data)
        if(data.error) {
            this.setState(
                Object.assign({}, this.state, {submitLoading: false})
            )
            return
        }
        this.performSubmit()
    }

    loginClosedCallback(e) {
        console.log('popup was closed')
        this.setState(
            Object.assign({}, this.state, {submitLoading: false})
        )        
    }

    async performSubmit() {
        let json = {'points': []}
        this.state.chart.points.forEach(function(point) {
            json.points.push({
                energy: point.y,
                minute: point.x
            })
        })
        let response = await fetch('/api/lines', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(json)            
        })
        let jsonData
        jsonData = await response.json()
        console.log(jsonData)
        this.setState(
            Object.assign({}, this.state, {submitLoading: false})
        )                
        
    }

    handleSubmit(e) {
        spotifyLoginPopup(
            'http://localhost:8000/spotify/authorize',
            this.loginCallback.bind(this),
            this.loginClosedCallback.bind(this)
        )
        this.setState(
            Object.assign({}, this.state, {submitLoading: true})
        )

    }
    
    render() {
        return (
            <div>
                <EditableChart config={this.props.chartConfig}></EditableChart>
                <SubmitButton
                    label="Make playlist"
                    onClick={this.handleSubmit.bind(this)}
                    disabled={this.state.submitLoading}
                >
                </SubmitButton>
                {this.state.submitLoading ? (<LoadingSpinner />) : (<div></div>)}
                {(this.state.playlistUrl && !this.state.submitLoading) ? (
                     <PlaylistResult url={this.state.playlistUrl} /> ) : ( <div></div>
                     )
                }
                
            </div>
            
        )
    }
}

/**
 * @param {string} url - url for the popup window
 * @param {function} messageCallback - callback for postMessage from popup ( receives event)
 * @param {function} closedCallback - callback when popup is closed prematurely (optional)
**/
function spotifyLoginPopup(url, messageCallback, closedCallback=null) {
    var width = 450,
	height = 730,
	left = (window.innerWidth / 2) - (width / 2),
	top = (window.innerHeight / 2) - (height / 2);

    function callback(e) {
        console.log('message')
        messageCallback(e)
        clearInterval(timer)
        e.source.close()
        window.removeEventListener('message', callback, false)
    }
    
    window.addEventListener('message', callback, false)
    let popup = window.open(
        url, 'Spotify login',
    	'menubar=no,location=no,resizable=no,scrollbars=no,status=no, width=' +
	width + ', height=' +
	height + ', top=' +
	top + ', left=' + left
    )    

    function windowClosedCallback() {
        if(closedCallback != null) {            
            closedCallback()
        }
        window.removeEventListener('message', callback, false)
    }

    var timer = setInterval(checkChild, 500);

    function checkChild() {
        if (popup.closed) {
            windowClosedCallback()
            clearInterval(timer);
        }
    }    
}


class App extends Component {
  render() {
    return (
        <div className="App">
            <ChartFormContainer chartConfig={chartConfig}></ChartFormContainer>
        </div>
    );
  }
}

export default App;
