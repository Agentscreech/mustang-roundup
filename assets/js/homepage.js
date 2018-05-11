import React, { Component } from 'react';
import {Link} from 'react-router-dom';
var auth = require('./auth')
import Results from './components/results'



class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.show_public = this.show_public.bind(this)
    }

    componentWillMount(){
        this.show_public()
    }
    show_public(){
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
        .then(function(res){
            this.setState(res)
        }
        .bind(this))
    }

    render() {
        if (auth.loggedIn()){
            var button = <Link to="/roundup"><span className="btn btn-primary">View Roundup</span></Link>
        } else {
            var button = <Link to="/login"><span className="btn btn-primary">Login</span></Link>
        }
        if (this.state.show){
            var results = <Results/>
        } else {
            var results = ""
        }
        return (
            <div className="text-center">
                <div className="row">
                    <div className="col">
                        <img src="/assets/img/logo.png"/>
                    </div>
                </div>
                    <div className="col">
                        {button}
                    </div>
                {results}
            </div>
        )
    }
}

export default HomePage
