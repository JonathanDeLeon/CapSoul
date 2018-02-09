import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';

import { Home, Login, Create, Profile, CapsoulPage, CapsoulEditPage, ProfileEdit } from './routes/index';
import './App.css';
import { MainNav, Auth} from "./components/index";
import { Container, Row, Col } from 'reactstrap';


class App extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    var navsw = <MainNav/>;
    if(window.location.pathname === "/"){
      navsw = "";
    }
    return (

      <div>
        {navsw}
        <Container>
          <Switch>
            <Route exact path='/' component={Login} />

            <Route path='/home' component={Home} />

            <Route path='/capsoul/edit/:cid' component={CapsoulEditPage} />
            <Route path='/capsoul/:cid' component={CapsoulPage} />

            <Route path='/create' component={Create} onEnter={this.requireAuth}/>
            <Route path='/profile/edit' component={ProfileEdit} />
            <Route path='/profile' component={Profile} />
            </Switch>
          </Container>
      </div>
    );
  }
}

export default App;
