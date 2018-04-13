import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Sidebar extends Component {
    constructor(props) {
        super(props)
        // this.state = {"links":[]}
        this.linkMaker = this.linkMaker.bind(this)
    }

    // componentDidMount(){
    //     this.setState({ "links": this.linkMaker(this.props.divisions)})
    // }

    linkMaker(names){
        // console.log(names)
        let links = []
        for (var i = 0; i < names.length; i++){
            let link = "/roundup/"+names[i].split(" ").join("").toLowerCase()
            let name = names[i]
            links.push(
                <li key={i} className="nav-item">
                    <Link className="nav-link" to={link}>{name}</Link>
                </li>
            )
        }
        return links
    }

    render(){
        let links = this.linkMaker(this.props.divisions)
        return (
            <nav className="col-sm-2 d-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <h6 className="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                        <Link className="nav-link" to="/roundup/">Results</Link>
                    </h6>
                    <h6 className="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">Divisions</h6>
                    <ul className="nav flex-column">
                        {links}
                    </ul>

                </div>

            </nav>
        )
    }
}

export default Sidebar