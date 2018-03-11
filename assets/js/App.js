import React, { Component } from 'react';

import { BrowserRouter as Router } from 'react-router-dom'

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
                        <h1>MUSTANG ROUND UP SITE</h1>
                    </div>
                </header>
            </div>
        )
    }
}

export default App
