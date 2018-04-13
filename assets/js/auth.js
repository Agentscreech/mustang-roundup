module.exports = {
    login: function (username, pass, cb) {
        this.getToken(username, pass, (res) => {
            if (res.authenticated) {
                localStorage.token = res.token
                if (cb) cb(res)
            } else {
                console.log("login callback ", cb)
                if (cb) cb(res)
            }
        })
    },

    logout: function () {
        delete localStorage.token
    },

    loggedIn: function () {
        return localStorage.token
    },

    getToken: function (username, pass, cb) {
        const params = {
            'method': 'post',
            'headers': new Headers({
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest'
            }),
            'body': JSON.stringify({
                username: username,
                password: pass
            })
            
        }

        fetch('/obtain-auth-token/', params)
        .then(res => res.json())
        .catch(error => {
                console.log(error);
                return cb({ authenticated: false })
        }) 
        .then(response => {
            console.log(response);
            if (response.token){
                return cb({
                    authenticated: true,
                    token: response.token
                })
            } else {
                return cb({ authenticated: false, response:response.non_field_errors[0]})
            }
        }) 
    }
}
