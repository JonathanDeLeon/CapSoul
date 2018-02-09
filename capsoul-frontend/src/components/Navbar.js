import React, { Component } from 'react';
import { history } from 'react-router-dom';
import { Collapse, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';

import { Auth } from './index';

export class MainNav extends React.Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }
    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }
    logout() {
        Auth.removeAuth();
    }
    render() {
        return (
            <div>
                <Navbar color="primary" light expand="md">
                    <NavbarBrand href="/home">CapSoul</NavbarBrand>
                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} navbar>
                        <Nav className="ml-auto" navbar>
                            <NavItem>
                                <NavLink href="/create">Create CapSoul</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/profile/">Profile</NavLink>
                            </NavItem>
                            <NavItem>
                              <NavLink href="#" onClick={this.logout}>Logout</NavLink>
                            </NavItem>
                        </Nav>
                    </Collapse>
                </Navbar>
            </div>
        );
    }
}
