import React, { Component } from 'react';

import ReactTable from 'react-table'
import 'react-table/react-table.css'

class Division extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.handleVote = this.handleVote.bind(this)
    
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
                temp[category].push({ name: res[i].name, car: res[i].car, votes: res[i].votes, voteButton: this.makeVoteButton(res[i].poll_id)})
            } else {
                temp[category] = [{ name: res[i].name, car: res[i].car, votes: res[i].votes, voteButton: this.makeVoteButton(res[i].poll_id)}]
            }

        }
        this.setState({categories: temp})
    }

    makeVoteButton(id){
        return (
            <button onClick={this.handleVote} data_id={id} className="btn btn-success">Vote</button>
        )
    }

    handleVote(e){
        var id = e.target.getAttribute('data_id')
        const params = {
            'method': 'post',
            'credentials': 'include',
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
        fetch('/poll/' + id+"/", params).then(function (res) {
                // console.log('poll response res: ', res, this)
                this.getDivision()
        }.bind(this))
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
        },
        {
            Header: 'Vote',
            accessor:'voteButton'
        }]
        let elements = []
        for (var category in this.state.categories){
            elements.push(
                <div key={category} className="text-center">
                    {category}
                    <ReactTable
                        data={this.state.categories[category]}
                        columns={columns}
                        showPagination = {false}
                        defaultPageSize = {this.state.categories[category].length}
                    />
                </div>
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
