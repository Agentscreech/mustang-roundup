import React, { Component } from 'react';
import {Link} from 'react-router-dom';
var auth = require('./auth')


class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }


    render() {
        if (auth.loggedIn()){
            var button = <Link to="/roundup"><span className="btn btn-primary">View Roundup</span></Link>
        } else {
            var button = <Link to="/login"><span className="btn btn-primary">Login</span></Link>
        }
        return (
            <div className="text-center">
                <h1>THIS IS THE HOMEPAGE</h1>
                    {button}
            </div>
        )
    }
}

export default HomePage
