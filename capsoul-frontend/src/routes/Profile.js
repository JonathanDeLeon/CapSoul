import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import {Col, Row} from 'reactstrap';

import { SERVER_URL } from '../config';
import { Auth, Image } from '../components/index';


export class Profile extends React.Component {
  constructor(props) {
    super(props);
    if(!Auth.isAuth()) {
      this.props.history.replace("/");
    }
    this.state = {
      user: null
    }
  }

  componentDidMount() {
    Auth.getUser().then(user =>{
      this.setState({ "user": user});
    })
  }

  render() {
    return (
      <div>
        <header>
          <br/>
          <h1>Your Profile</h1>
          <hr />
        </header>
        <ProfileRender user={this.state.user}/>
        <Link to="/profile/edit" >Edit Profile</Link>
      </div>
    )
  }
}

function ProfileRender(props) {
  let user = props.user;
  if(user) {
    return(
      <div>
        <Row>
            <Col sm="12" md={{size: 4, offset: 4}}>
                <Image uri={"/users/media/" + user.username} className="rounded-circle img-fluid"/>
            </Col>
        </Row>
        <ul>
          <li> First Name: {user.first_name} </li>
          <li> Last Name: {user.last_name} </li>
          <li> Birthdate: {user.date_of_birth} </li>
          <li> Email: {user.email} </li>
          <li> Phone: {user.phone} </li>
          <li> Location: {user.location} </li>
        </ul>
      </div>
    )
  } else {
    return (<div> No user....</div>)
  }
}
