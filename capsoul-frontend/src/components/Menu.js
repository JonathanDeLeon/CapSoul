import React, { Component } from 'react';
import { Link } from 'react-router-dom';


export class Menu extends Component {
    render() {
        return (
            <div id="MenuOptions">
                <Link to="/home" className="Menu" id="Home">Home</Link>&nbsp;
                <Link to="/create" className="Menu" id="CreateCapSoul">Create CapSoul</Link>&nbsp;
                <Link to="/profile" className="Menu" id="Profile">Profile</Link>
            </div>
        );
    }
}
