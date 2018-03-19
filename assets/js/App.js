import React, { Component } from 'react';
import Login from './login'
import HomePage from './homepage'
import Roundup from './roundup'
import { BrowserRouter as Router, Route } from 'react-router-dom'

var auth = require('./auth')

function requireAuth(nextState, replace) {
    if (!auth.loggedIn()) {
        replace({
            pathname: '/login',
            state: { nextPathname: '/roundup/' }
        })
    }
}

class App extends Component{
    constructor(props){
        super(props);
        this.state = {}
    }

    render(){
        return (
            <div>
                <header>
                    <div className="row">
                        <div className="col-12">
                            <h1 className="text-center">MUSTANG ROUND UP SITE</h1>
                        </div>
                    </div>
                </header>
                <Router>
                    <div>
                        <Route exact path="/" component={HomePage}/>
                        <Route path="/login" component={Login} />
                        <Route path="/roundup" component={Roundup} onEnter={requireAuth} />
                    </div>
                </Router>
            </div>
        )
    }
}

export default App
