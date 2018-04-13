import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'


class Results extends Component {
    constructor(props) {
        super(props);
        this.state = {}
        this.buildCategories = this.buildCategories.bind(this)
    }

    componentWillMount(){
        const params = {
            'method': 'get',
            'credentials': 'include',
            'headers': new Headers({
                // 'X-CSRFToken': csrftoken,
                "Accept": "application/json",
                "Content-Type": "application/json",
                'X-Requested-With': 'XMLHttpRequest',
                'Authorization': 'Token ' + localStorage.token
            }),
        }
        fetch('/standings/', params).then((res) => res.json())
        .then( function (res) {
            console.log('standing response ', res)
            // this.setState({"entries":res.entries})
            var entries = res.entries
            var divisions = []
            for (var i = 0; i < entries.length; i++){
                var div = Object.keys(entries[i])[0]
                divisions.push(this.buildCategories(div, entries[i][div]))
            }
            this.setState({ "divs": divisions })

        }.bind(this))
    }

    buildCategories(divName, categories) {
        const columns = [{
            Header: 'Name',
            accessor: 'name'
        }, {
            Header: 'Car',
            accessor: 'car',
        }
        ]
        let elements = []
    
        for (var i = 0; i < categories.length; i++) {
            let _max = 0
            var category = Object.keys(categories[i])[0]
            var entries = categories[i][category]
            var list = []
            for (var j = 0; j < entries.length; j++) {
                    list.push(entries[j])
            }
            if (list.length > _max) {
                _max = list.length
            }
            elements.push(
                <div key={category} className="text-center">
                    {category}
                    <ReactTable
                        data={list}
                        columns={columns}
                        showPagination={false}
                        defaultPageSize={_max}
                    />
                </div>
            )
        }
        var thing = <div className="text-center">
            <h3>{divName} Division</h3>
            {elements}
        </div>
        console.log(thing)
        return thing
    }

    render() {

        return <div className="col">
                    <h4 className="text-center">Click on a division on the right to show cars entered in that division</h4>
                    {this.state.divs}
            </div>

    }

}

export default Results