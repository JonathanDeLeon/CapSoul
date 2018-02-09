import React, { Component } from 'react';
import axios from 'axios';
import { Col } from 'reactstrap';

import { SERVER_URL } from '../../../config';

// TODO:50 Build edit/delete funcitonality.
export class LetterComponent extends Component {
  constructor(props){
    super(props);
    this.state = {"letter": null, "isEdit":false};
    axios.get(SERVER_URL + "/capsules/letters/" + props.lid).then(response => {
      let state = this.state;
      state.letter = response.data;
      this.setState(state);
    })

    //bind 'this' to the following functions.
    this.delete = this.delete.bind(this);
  }

  //Deletes this comment.
  delete() {
    // Axios remove request then trigger reload function.
    if(window.confirm("Are you sure you would like to delete this letter?")){
      axios.delete(SERVER_URL + "/capsules/letters/" + this.props.lid).then((res) => {
        if(res.data.status === "letter deleted") {
          this.props.reload();
        }
      }).catch((er) => {
        alert(er);
      })
    }
  }

  render() {
    if(this.state.letter){
      return(
        <div className="card bg-light sm-12 md-4 lg-3">
          <div className="card-body">
            <h4 className="card-title">{this.state.letter.title}</h4>
            <p className="card-text">{this.state.letter.text}</p>
            <button onClick={this.delete} className="btn btn-danger btn-sm">Delete</button>
          </div>
        </div>
      )
    } else {
      return(
        <div>Loading letter...</div>
      )
    }

  }
}
