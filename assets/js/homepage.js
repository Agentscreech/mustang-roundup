import React, { Component } from 'react';
import {Link} from 'react-router-dom';

class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    render() {
        return (
            <div>
                <h1>THIS IS THE HOMEPAGE</h1>
                <div className="btn btn-primary">
                    <Link to="/login">Login</Link>
                </div>
            </div>
        )
    }
}

export default HomePage
