import React, { Component } from 'react';
import axios from 'axios';
import Select from 'react-select';
import 'react-select/dist/react-select.css';


import { Auth } from './index';
import { SERVER_URL } from '../config';

// TODO: Make this work.
export class UserListComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedUsers: null,
      options: [],
      currentUser: null
    }
    if(this.props.init) {
      this.state.selectedUsers = this.props.init.map((userString) =>{
        return({"value": userString, "label": userString})
      });
    }
    //Get all the users and create options[] for the <Select/> object.
    axios.get(`${SERVER_URL}/users`).then((res) => {
      let state = this.state;
      // Convert user[] to options[].
      let options = res.data.users.map((usr) => {
        if(usr.first_name && usr.last_name){
          return ({ "value": usr.username,
            "label": `${usr.first_name} ${usr.last_name}`
          })
        } else {
          return({
            "value":usr.username,
            "label":usr.username
          })
        }
      });
      state.options = options;
      this.setState(state);
    }).catch((er) => alert(er));

    Auth.getUser().then((user) => {
      let state = this.state;
      state.currentUser = user;
      this.setState(state);
    });
  }

  // Get the changes from <Select/> and send them to the parent component.
  handleChange = (selectedUsers) => {
    let state = this.state;
    state.selectedUsers = selectedUsers;
    this.setState(state);
    console.log(`Selected: ${selectedUsers}`);
    console.log(selectedUsers);
    let users = selectedUsers.map((user) => {
      return(user.value);
    })
    this.props.callback(users);
  }

  render() {
    //remove disabled[] and currentUser from options[]
    let options = this.state.options;
    if(this.props.disabled && Array.isArray(this.props.disabled)) {
      options = options.filter((opt) => {
        let pass = !this.props.disabled.includes(opt.value)
        if(this.state.currentUser){
          pass = pass && opt.value !== this.state.currentUser.username
        }
        return pass;
      });
    }
    return (
      <Select
        name="form-field-name"
        value={this.state.selectedUsers}
        onChange={this.handleChange}
        options={options}
        multi
        placeholder="Start typing a name..."
      />
    );
  }
}
