import React, { Component } from 'react';
import Login from './login'
import HomePage from './homepage'
import Roundup from './roundup'
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom'

var auth = require('./auth')


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
                    <Switch>
                        <Route exact path="/" component={HomePage}/>
                        <Route path="/login" component={Login} />
                        <Route path="/roundup" render={() => (
                            auth.loggedIn() ? (
                                <Roundup/>
                            ) : (<Redirect to="/login" />)
                        )} />
                        <Route path='*' render={() => (<Redirect to="/"/>)}/>
                    </Switch>
                </Router>
            </div>
        )
    }
}

export default App
