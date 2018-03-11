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
                        <div className="col-12">
                            <h1 className="text-center">MUSTANG ROUND UP SITE</h1>
                        </div>
                    </div>
                </header>
            </div>
        )
    }
}

export default App
