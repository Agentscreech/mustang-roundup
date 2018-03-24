import React, { Component } from 'react';


class Category extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    
    }




    render(){
        return <div>{this.props.name} Section</div>

    }

}

export default Category