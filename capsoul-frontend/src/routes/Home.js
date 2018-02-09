import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import { Auth, Countdown } from '../components/index';
import { SERVER_URL } from '../config';
import { Card, CardImg, CardImgOverlay, CardText, CardBody,
  CardTitle, CardSubtitle, CardLink, CardHeader, CardFooter,
  Button, Row, Col, Jumbotron } from 'reactstrap';


export class Home extends React.Component {
    constructor(props) {
        super(props);
        if(!Auth.isAuth()) {
          this.props.history.replace("/");
        }
        this.state = {"MyCapsules":[], "UnlockedCapsules":[], "LockedCapsules":[]};
        Auth.getUser().then((usr) => {
          let username = usr.username;
          // TODO: This logic needs to be changed. Unlocked Capsules and Locked Capsules show every open or locked capsule.
          axios.get(SERVER_URL + "/capsules").then(response =>{
              var DateNow = new Date();
              var MyCapsules = response.data.capsules.filter(function(capsule){
                  var UnlockDate = new Date(capsule.unlocks_at);
                  return (UnlockDate.getTime() > DateNow.getTime() && (capsule.owner === username));
              });
              var UnlockedCapsules = response.data.capsules.filter(function(capsule){
                  var UnlockDate = new Date(capsule.unlocks_at);
                  return (UnlockDate.getTime() < DateNow.getTime() && (capsule.owner !== username) && (capsule.recipients.includes(username)));
              });
              var LockedCapsules = response.data.capsules.filter(function(capsule){
                  var UnlockDate = new Date(capsule.unlocks_at);
                  return (UnlockDate.getTime() > DateNow.getTime() && (capsule.owner !== username) && (capsule.recipients.includes(username)));
              });


              this.setState({"MyCapsules": MyCapsules, "UnlockedCapsules":UnlockedCapsules, "LockedCapsules":LockedCapsules});
          })
        })

    }
    render() {
        return (
            <div>
                <header>
                <br/>
                </header>

                <Card body className="text-center">
                  <CardTitle>My CapSouls</CardTitle>
                  <CapSouls header="My CapSouls" capsules={this.state.MyCapsules} />
                </Card>

                <br/>

                <Card body className="text-center">
                  <CardTitle>Unlocked CapSouls</CardTitle>
                  <CapSouls header="Unlocked CapSouls" capsules={this.state.UnlockedCapsules} />
                </Card>

                <br/>

                <Card body className="text-center">
                  <CardTitle>Locked CapSouls</CardTitle>
                  <CapSouls header="Locked CapSouls" capsules={this.state.LockedCapsules} />
                </Card>
            </div>
        )
    }
}

/*
 This class creates a CapSouls for all three CapSoul types depending on what header is passed in
 (Yet to be implemented: changing the caption to CapSouls when they are present, changing to view page when
 'view more' is pressed, view individual CapSoul when CapSoul is selected)
 */
class CapSouls extends Component {
    constructor() {
        super();
    }

    render() {

        if (this.props.capsules.length === 0) {
            return (
                <div>
                    <p>No CapSouls</p>
                </div>
            );
        } else {
            return (
                <div>
                    <Row>
                    {
                        this.props.capsules.map((capsule, i) => {
                            var link;
                            var countd = "";
                            var unlock_form = <span>Unlocks at: </span>;
                            var displayDateTime = new Date(capsule.unlocks_at).toLocaleString();
                            if(this.props.header !== "Unlocked CapSouls"){
                              countd = <Countdown time={capsule.unlocks_at}/>;
                            }
                            if(this.props.header === "My CapSouls") {

                              link = <span>
                                  <Link to={"/capsoul/edit/" + capsule.cid}>Edit</Link>
                                  &#160;&#160;
                                  <Link to={"/capsoul/" + capsule.cid }>Open</Link>
                              </span>;
                          } else if (this.props.header === "Unlocked CapSouls"){
                              link = <Link to={"/capsoul/" + capsule.cid }>Open</Link>;
                              unlock_form = <span>Unlocked at: </span>;
                            }
                            if(this.props.header !== "Open CapSouls"){

                            }
                            return (
                              <Col key={i} sm="3">
                                <Card>
                                <CardHeader>{capsule.title}</CardHeader>
                                <CardBody>
                                  <CardImg top width="100%" src="CapSoulLogo.png" alt="Card image cap" />
                                    {link}
                                  </CardBody>
                                  <CardFooter>
                                  {unlock_form}<div>{displayDateTime}</div>
                                  {countd}
                                  </CardFooter>
                                </Card>
                              </Col>
                            )
                        })
                    }
                </Row>
                </div>
            );
        }
    }
}
