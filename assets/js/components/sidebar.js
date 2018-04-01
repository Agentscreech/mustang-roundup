import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Sidebar extends Component {
    constructor(props) {
        super(props)
    }


    render(){
        return (
            <nav className="col-sm-2 d-block bg-light sidebar">
                <div className="sidebar-sticky">
                    <ul className="nav flex-column">
                        {/* make this dynamic by looking at what divisions are returned from the DB */}
                        <li className="nav-item">
                            <Link className="nav-link" to="/roundup/BestinShow">Best in Show</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/roundup/ConcourseTrailered">Concourse Trailered</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/roundup/ConcourseDriven">Concourse Driven</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to="/roundup/DailyDriven">Daily Driven</Link>
                        </li>

                    </ul>

                </div>

            </nav>
        )
    }
}

export default Sidebar