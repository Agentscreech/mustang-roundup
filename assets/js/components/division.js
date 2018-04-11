import React, { Component } from 'react';

import ReactTable from 'react-table'
import 'react-table/react-table.css'

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
                // console.log('division res: ', res)
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
                temp[category].push({name:res[i].name, car:res[i].car, votes:res[i].votes})
            } else {
                temp[category] = [{name:res[i].name, car:res[i].car, votes:res[i].votes}]
            }

        }
        this.setState({entries: res, categories: temp})
    }

    buildCategories(){
        const columns = [{
            Header: 'Name',
            accessor: 'name'
        }, {
            Header: 'Car',
            accessor: 'car',
        },
        {
            Header: 'Votes',
            accessor: 'votes'
        }]
        let elements = []
        for (var category in this.state.categories){
            elements.push(
                <ReactTable
                    data={this.state.categories[category]}
                    columns={columns}
                    showPagination = {false}
                    defaultPageSize = {this.state.categories[category].length}
                    key ={category}
                />
            )
        }
        return elements
    }


    render(){
        var elements = this.buildCategories()
        return <div className="col">
                    <h3 className="text-center">{this.props.name} Division</h3>
                    {elements}
                </div>

    }

}

export default Division
