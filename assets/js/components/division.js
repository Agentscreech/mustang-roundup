import React, { Component } from 'react';

import ReactTable from 'react-table'
import 'react-table/react-table.css'

class Division extends Component {
    constructor(props) {
        super(props);
        this.state = {categories: ""}
        this.handleVote = this.handleVote.bind(this)
        this.handleChange = this.handleChange.bind(this)
    }
    componentWillMount() {
        this.getDivision()
    }
    handleChange(event){
        console.log(event.target.id, event.target.value)
        var id = event.target.id
        var points = event.target.value
        var obj = {}
        obj[id] = points
        console.log(obj)
        this.setState(obj)
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

        }
        fetch('/division/'+this.props.name, params).then(res => res.json())
            .then(function (res) {
                this.findCategories(res)
            }.bind(this)
            )
    }

    findCategories(res){
        let temp = {}
        for (var i = 0; i < res[0].length; i++){
            var obj = {}
            obj[res[0][i].poll_id] = res[0][i].votes.toString()
            this.setState(obj)
            if (this.props.name == "People's Choice"){
                res[0][i]["voteButton"] = this.makeVoteButton(res[0][i].poll_id, "Vote")
                res[0][i]['points'] = res[0][i]['votes']
            } else {
                res[0][i]["voteButton"] = this.makeVoteButton(res[0][i].poll_id, "Submit")
                res[0][i]["points"] = this.makeInputfield(res[0][i])
            }
        }
        this.setState({entries: res[0], categories:res[1]})
    }

    makeInputfield(entry){
        return (
            <input className="text-center" type="number" defaultValue={entry.votes} id={entry.poll_id} key={entry.id} />
        )
    }

    makeVoteButton(id, text){
        return (
            <button onClick={this.handleVote} data_id={id} className="btn btn-success">{text}</button>
        )
    }

    handleVote(e){
        var id = e.target.getAttribute('data_id')
        console.log(id)
        if (this.props.name == "People's Choice"){
            var entries = this.state.entries
            var points;
            entries.forEach(function (entry) {
                if (entry.poll_id == id) {
                    entry.points++
                    points = entry.points
                }
            });
            this.setState({ entries: entries })
        } else {
            var points = document.getElementById(id).value
        }
        
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
            'body': JSON.stringify({
                points: points,
            })

        }
        fetch('/poll/' + id+"/", params).then(function (res) {
                // console.log('poll response res: ', res, this)
                // this.getDivision()
        }.bind(this))
    }

    buildCategories(){
        const columns = [{
            Header: 'Number',
            accessor: 'entry_number'
        },{
            Header: 'Name',
            accessor: 'name'
        }, {
            Header: 'Car',
            accessor: 'car',
        },
        {
            Header: 'Points',
            accessor: 'points'
        },
        {
            Header: 'Submit Points',
            accessor:'voteButton'
        }]
        let elements = []
        if (Object.keys(this.state.categories).length > 0){
            for (var i = 0; i < this.state.categories.length; i++) {
                let _max = 0
                var category = this.state.categories[i]
                var entries = []
                for (var j = 0; j < this.state.entries.length; j++) {
                    if (this.state.entries[j].category == category) {
                        entries.push(this.state.entries[j])
                    }
                }
                if (entries.length > _max){
                    _max = entries.length
                }
                elements.push(
                    <div key={category} className="text-center">
                        {category}
                        <ReactTable
                            data={entries}
                            columns={columns}
                            showPagination={false}
                            defaultPageSize={_max}
                            defaultSorted={[
                                {
                                    id: "points",
                                    desc: true
                                }
                            ]}
                        />
                    </div>
                )
            }
            return elements
        } else {
            return ""
        }
        
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
