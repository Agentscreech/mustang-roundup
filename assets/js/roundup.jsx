import React, { Component } from 'react';
var auth = require('./auth')
import Division from './components/division'
import Sidebar from './components/sidebar'
import Results from './components/results'
import {
    Router,
    Route,
    Switch,
} from 'react-router-dom'

class Roundup extends Component {
    constructor(props) {
        super(props);
        this.state = { 
            'user': [],
            'divisions': []
        }
        this.loadUserData = this.loadUserData.bind(this)
        this.logoutHandler = this.logoutHandler.bind(this)
        this.goHome = this.goHome.bind(this)
        this.toggleLive = this.toggleLive.bind(this)
        this.show_public = this.show_public.bind(this)
    }

    componentDidMount() {
        this.loadUserData()
    }
    
    componentWillMount(){
        this.getDivisions()
        this.show_public()

    }

    logoutHandler() {
        auth.logout()
        this.props.history.replace('/login/')
    }

    goHome(){
        this.props.history.replace('/')
    }

    show_public() {
        const params = {
            'method': 'get',
            // 'credentials': 'include',
            'headers': new Headers({
                // 'X-CSRFToken': csrftoken,
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Token ' + localStorage.token
            }),

        }
        fetch('/show_public/', params)
            .then(res => res.json())
            .then(function (res) {
                this.setState(res)
            }
                .bind(this))
    }

    loadUserData(){
        const params = {
            'method': 'get',
            'headers': new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Token ' + localStorage.token
            }),

        }
        fetch('/users/i/',params).then(res => res.json())
        .then(function(res)
            {
                this.setState({ user: res })
            }.bind(this)
        )  
    }
    getDivisions(){
        const params = {
            'method': 'get',
            'headers': new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Token ' + localStorage.token
            }),

        }
        fetch('/getDivisions/', params).then(res => res.json())
            .then(function (res) {
                this.setState({ divisions: res })
            }.bind(this)
            )  
    }

    buildRoutes(divisions){
        var routes = [<Route exact key="0" path="/roundup/" render={(props) => (
            <Results />
        )} />]
        for (var i = 0; i < divisions.length; i++){
            let divpath = "/roundup/" + divisions[i].split(" ").join("").toLowerCase()
            let name = divisions[i]
            routes.push(<Route key={i+1} path={divpath} render={(props) => (
                        <Division name={name} />
                    )}/>
                )
        }
        return routes
    }
    
    toggleLive(){
        // console.log(this.state)
        const params = {
            'method': 'post',
            'headers': new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Token ' + localStorage.token
            }),
            'body': JSON.stringify({
                toggle: !this.state.show
            })

        }
        fetch('/toggle_show/', params).then(function(res){
            this.setState({'show': !this.state.show})
        }.bind(this))
    }
    render() {
        let routes = this.buildRoutes(this.state.divisions)
        if (this.state.show){
            var toggle = <button className="btn btn-success" id="toggleButton" onClick={this.toggleLive}>Toggle Live Off</button>
        } else {
            var toggle = <button className="btn btn-success" id="toggleButton" onClick={this.toggleLive}>Toggle Live On</button>

        }

        return (
            <div className="col-12">
                {/* <h4 className="text-center">You are logged in as {this.state.user.username}</h4> */}
                <div className="row justify-content-between">
                    <button className="btn btn-primary" onClick={this.goHome}>Home</button>
                    {toggle}
                    <button className="btn btn-danger" onClick={this.logoutHandler}>Log out</button>
                </div>
                
                <div className="row">
                    <Sidebar divisions={this.state.divisions}/>
                    <Switch>
                        {routes}                        
                    </Switch>
                </div>
            </div>

            
        )
    }
}

export default Roundup
