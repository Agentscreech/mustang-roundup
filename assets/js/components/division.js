import React, { Component } from 'react';


class Division extends Component {
    constructor(props) {
        super(props);
        this.state = {
            entries: [{
                "car" : "",
                "category" : "",
                "name" : ""

            }]
        }
    
    }
    componentDidMount() {
        this.getDivision()
    }

    getDivision(){
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
            // 'body': JSON.stringify({
            //     username: username,
            //     password: pass
            // })

        }
        fetch('/test/', params).then(res => res.json())
            .then(function (res) {
                console.log('division res: ', res)
                this.setState({ entries: res })
            }.bind(this)
            )  
    }




    render(){
        var category = this.state.entries[0].category
        var name = this.state.entries[0].name
        var car = this.state.entries[0].car

        return <div>{this.props.name} Section
            <div>{category || ""}
                <div>{name || ""} {car || ""}</div>
            </div>

        </div>

    }

}

export default Division