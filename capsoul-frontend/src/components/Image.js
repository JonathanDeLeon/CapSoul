import React, { Component } from 'react';
import axios from 'axios';

import { SERVER_URL } from '../config';

// TODO: make the image show up in correct orientaion.
// NOTE: This library might help [https://github.com/blueimp/JavaScript-Load-Image]
export class Image extends Component {
  constructor(props){
    super(props);
    this.state = {
      "src": null
    }
    axios.get(SERVER_URL + this.props.uri, {
      responseType: "blob"
    }).then((res) => {
      let state = this.state;
      state.src = URL.createObjectURL(res.data);
      this.setState(state);
    });
  }
  render() {
    return(
      <img src={this.state.src} alt="Profile Photo" className={this.props.className}/>
    )
  }
}
