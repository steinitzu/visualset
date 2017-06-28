import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import HighCharts from 'highcharts'
import makeDraggable from 'highcharts-draggable-points'
import ReactHighCharts from 'react-highcharts'
import chartConfig from './ChartConfig'

import { StyledSubmit } from './Styles'


// monkey patching or something
makeDraggable(HighCharts)


class Title extends Component {
    render() {
        return (
            <h2>
                Move the points on the line to control song intensity.  
            </h2>
        )
    }
}


class SubmitButton extends Component {
    render() {
        return (            
            <StyledSubmit
                type="button"
                onClick={this.props.onClick}
                disabled={this.props.disabled}>
                {this.props.label}
            </StyledSubmit>
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
            <iframe src="https://open.spotify.com/embed?uri=spotify:user:erebore:playlist:788MOXyTfcUb1tdw4oC7KJ"
                    width="250" height="80" frameborder="0" allowtransparency="true">
                
            </iframe>
        )
        return (
            <a href={this.props.url} target="_blank"
               rel="noopener noreferrer">
                Your playlist is here!
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
        console.log(chart)
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
        let data
        try {
            data = JSON.parse(e.data)
        } catch (e) {
            return
        }
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
        this.setState(
            Object.assign({}, this.state, {submitLoading: false})
        )
        this.setState(
            Object.assign(
                {}, this.state,
                {playlistUrl: jsonData.external_urls.spotify}
            )
        )
    }

    handleSubmit(e) {
        spotifyLoginPopup(
            process.env.REACT_APP_SPOTIFY_AUTH_URL,
            this.loginCallback.bind(this),
            this.loginClosedCallback.bind(this)
        )
        this.setState(
            Object.assign({}, this.state, {submitLoading: true})
        )
    }
    
    render() {
        const { submitLoading, playlistUrl } = this.state
        console.log('playlistUrl', playlistUrl)
        return (
            <div>
                <Title></Title>
                <EditableChart
                    config={this.props.chartConfig}>
                </EditableChart>
                {(playlistUrl && !submitLoading) ? (
                     <PlaylistResult url={playlistUrl} /> ) : ( <div></div>
                     )
                }
                <SubmitButton
                    label="Make playlist"
                    onClick={this.handleSubmit.bind(this)}
                    disabled={this.state.submitLoading}
                >
                </SubmitButton>
                {submitLoading ? (<LoadingSpinner />) : (<div></div>)}
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
