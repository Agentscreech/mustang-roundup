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
            ).then(() => {
                // this.setState({cats:this.buildCategories()})

            })
    }

    findCategories(res){
        let temp = {}
        for (var i = 0; i < res[0].length; i++){
            res[0][i]["voteButton"] = this.makeVoteButton(res[0][i].poll_id)
        }
        this.setState({entries: res[0], categories:res[1]})
    }

    makeVoteButton(id){
        return (
            <button onClick={this.handleVote} data_id={id} className="btn btn-success">Vote</button>
        )
    }

    handleVote(e){
        var id = e.target.getAttribute('data_id')
        var entries = this.state.entries
        entries.forEach(function(entry) {
            if (entry.poll_id == id){
                entry.votes++
            }
        });
        this.setState({entries:entries})
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
                // this.getDivision()
        }.bind(this))
    }

    buildCategories(){
        console.log(this.state.categories)
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
        let _max = 0
        if (Object.keys(this.state).length > 0){
            for (var i = 0; i < this.state.categories.length; i++) {
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
                                    id: "votes",
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
