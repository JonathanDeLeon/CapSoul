import React, { Component } from 'react';
import axios from 'axios';
import { Col } from 'reactstrap';

import { SERVER_URL } from '../../../config';

// TODO:40 Build delete from server Logic.
export class MediaComponent extends Component {
  constructor(props){
    super(props);
    this.state = {
      "src": null
    }
    this.removeMedia = this.removeMedia.bind(this);

    axios.get(SERVER_URL + "/capsules/media/" + this.props.mid, {
      responseType: "blob"
    }).then((res) => {
      let state = this.state;
      state.src = URL.createObjectURL(res.data);
      this.setState(state);
    });
  }
  removeMedia() {
    if(window.confirm("Do you want to delete this image?")){
      axios.delete(SERVER_URL + "/capsules/media/" + this.props.mid).then((res) => {
        try {
          if(res.data.status === "media deleted"){
            this.props.reload();
          }
        } catch(e) {
          alert("there was a problem deleting the capsule: " + e);
        }
      }).catch((e) => alert("There was a problem deleting the capsule: " + e))
    }
  }
  render() {
    return(
        <div className="card bg-light border-light text-white sm-6 md-3">
          <img src={this.state.src} alt="Memory" className="card-img"/>
        </div>
    )
  }
}
