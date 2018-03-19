import React, { Component } from 'react';
var auth = require('./auth')
import { withRouter } from 'react-router-dom'

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    // contextTypes: {
    //     router: React.PropTypes.object.isRequired
    // },

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
        }
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <input type="text" placeholder="username" ref="username" />
                    <input type="password" placeholder="password" ref="pass" />
                    <input type="submit" />
                </form>
                {error}
            </div>
            
        )
    }
}

export default Login
