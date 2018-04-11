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
        fetch('/division/'+this.props.name, params).then(res => res.json())
            .then(function (res) {
                console.log('division res: ', res)
                // this.setState({ entries: res })
                this.findCategories(res)
            }.bind(this)
            )
    }

    findCategories(res){
        let temp = {}
        for (var i = 0; i < res.length; i++){
            let category = res[i].category
            if (category in temp){
                temp[category].append({name:res[i].name, car:res[i].car})
            } else {
                temp[category] = [{name:res[i].name, car:res[i].car, votes:res[i].votes}]
            }

        }
        this.setState({entries: res, categories: temp})
    }

    buildCategories(){
        let elements = []
        for (var category in this.state.categories){
            let entries = this.buildEntries(this.state.categories[category])
            elements.push(
                <div>
                    {category}
                    {entries}
                </div>
            )
        }
        return elements
    }

    buildEntries(entries){
        var temp = []
        for (var i = 0; i < entries.length; i++){
            temp.push(<span>
                Name: {entries[i].name} Car: {entries[i].car} Votes: {entries[i].votes}
            </span>)
        }
        return temp
    }


    render(){
        var category = this.state.entries[0].category
        var name = this.state.entries[0].name
        var car = this.state.entries[0].car
        var elements = this.buildCategories()
        return <div>{this.props.name} Section
                {elements}
                </div>

    }

}

export default Division