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
                    <Link to="/login"><span className="btn btn-primary">Login</span></Link>
            </div>
        )
    }
}

export default HomePage
