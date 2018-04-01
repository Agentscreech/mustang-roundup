import React, { Component } from 'react';
var auth = require('./auth')
import Division from './components/division'
import Sidebar from './components/sidebar'
import {
    Router,
    Route,
    Switch,
} from 'react-router-dom'

class Roundup extends Component {
    constructor(props) {
        super(props);
        this.state = { 'user': []}
        this.loadUserData = this.loadUserData.bind(this)
        this.logoutHandler = this.logoutHandler.bind(this)
    }

    // getInitialState() {
    //     return { 'user': [] }
    // }

    componentDidMount() {
        this.loadUserData()
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
                console.log('users response: ', res)
                this.setState({ user: res })
            }.bind(this)
        )  
    }

    render() {
        return (
            <div>
                <h1>You are now logged in, {this.state.user.username}</h1>
                <button onClick={this.logoutHandler}>Log out</button>
                    <div className="row">
                        <Sidebar />
                        <Switch>
                            <Route path="/roundup/BestinShow" render={(props) => (
                                <Division name="Best in Show" />
                            )}/>
                            <Route path="/roundup/ConcourseTrailered" render={(props) => (
                                <Division name="Concourse Trailered" />
                            )} />                            

                        </Switch>
                    </div>
            </div>

            
        )
    }
}

export default Roundup
