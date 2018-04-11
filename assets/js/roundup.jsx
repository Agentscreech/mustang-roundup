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
    }

    // getInitialState() {
    //     return { 'user': [] }
    // }

    componentDidMount() {
        this.loadUserData()
    }
    
    componentWillMount(){
        this.getDivisions()

    }

    // contextTypes: {
    //     router: React.PropTypes.object.isRequired
    // },

    logoutHandler() {
        auth.logout()
        this.props.history.replace('/login/')
    }

    loadUserData(){
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
            // 'body': JSON.stringify({
            //     username: username,
            //     password: pass
            // })

        }
        fetch('/users/i/',params).then(res => res.json())
        .then(function(res)
            {
                // console.log('users response: ', res)
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
            // 'body': JSON.stringify({
            //     username: username,
            //     password: pass
            // })

        }
        fetch('/getDivisions/', params).then(res => res.json())
            .then(function (res) {
                // console.log('division res: ', res)
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
    

    render() {
        let routes = this.buildRoutes(this.state.divisions)
        return (
            <div>
                <h1 className="text-center">You are now logged in, {this.state.user.username}</h1>
                <div><button onClick={this.logoutHandler}>Log out</button></div>
                
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
