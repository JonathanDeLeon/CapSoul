import React, { Component } from 'react';
import axios from 'axios';

import { SERVER_URL } from '../../../config';

export class CommentComponent extends Component {
  constructor(props){
    super(props);
    this.state = {"user": null}
    axios.get(SERVER_URL + "/users/" + props.comment.owner).then(response => {
      this.setState({"user": response.data });
    });
  }
  render() {
    let user = this.state.user;
    if(user && user.first_name && user.last_name){
      return(
        <p>{user.first_name} {user.last_name}: {this.props.comment.text}</p>
      )
    }
    return(
      <p>{this.props.comment.owner}: {this.props.comment.text}</p>
    )
  }
}
