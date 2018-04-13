import React, { Component } from 'react';
var auth = require('./auth')
import { withRouter } from 'react-router-dom'

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(e) {
        e.preventDefault()
        var username = this.refs.username.value
        var pass = this.refs.pass.value

        auth.login(username, pass, (loggedIn) => {
            if (loggedIn.authenticated) {
                this.props.history.push('/roundup')
            } else {
                this.setState({ login_error: loggedIn.response })
            }
        })
    }

    render() {
        if (this.state.login_error){
            var error = <p>{this.state.login_error}</p>
            setTimeout(() => {
                this.setState({ login_error: null})
            }, 3000);
        }
        return (
            <div className="row justify-content-center">
                <div className="col-6">
                    <form onSubmit={this.handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">Username:</label>
                            <input className="form-control" type="text" placeholder="Enter Username" ref="username" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password:</label>
                            <input className="form-control" type="password" placeholder="Enter Password" ref="pass" />
                        </div>
                            <input className="btn btn-primary" type="submit" />
                        
                    </form>
                    {error}
                </div>
            </div>
            
        )
    }
}

export default Login
