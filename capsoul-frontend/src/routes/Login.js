import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

import { SERVER_URL } from '../config';
import { Auth } from '../components/index';
import { Form, FormGroup, Input, Card, CardBody,
  CardTitle, CardDeck, Button, Col, Row, Jumbotron, Media } from 'reactstrap';


export class Login extends React.Component {
    constructor(props) {
        super(props);
        if(Auth.isAuth()) {
          this.props.history.replace("/home");
        }
        this.state = {"login": {
            "username": "",
            "password": ""
        }, "register": {
            "username": "",
            "password": "",
            "password1": "",
            "email": ""
        }};
        this.handleLoginChange = this.handleLoginChange.bind(this);
        this.handleRegisterChange = this.handleRegisterChange.bind(this);
        this.login = this.login.bind(this);
        this.register = this.register.bind(this);
    }
    handleLoginChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        let state = this.state;
        state.login[name] = value;
        this.setState(state);
    }
    handleRegisterChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        let state = this.state;
        state.register[name] = value;
        this.setState(state);
    }
    login(event) {
        event.preventDefault();
        console.log("login()");
        let cred = this.state.login;
        if(cred.username && cred.password) {
            axios.post(SERVER_URL + "/login/",
            {"username": cred.username, "password": cred.password}).then((res)=>{
                try {
                    if(res.data.status === "login successful") {
                        Auth.setAuth(res.data.token)
                        this.props.history.push("/home");
                    }
                } catch(e) {
                    console.log(e);
                    alert("There was a problem logging you in.");
                }

            }).catch((er) => {
              try {
                alert(er.response.data.status);
              } catch(e) {
                alert(er);
              }
            });
        } else {
            alert("Username or Password is blank.");
        }
    }
    register(event) {
        event.preventDefault();

        let reg = this.state.register;
        if(reg.password === reg.password1) {
            if(reg.username && reg.password && reg.email){
                axios.post(SERVER_URL + "/register/",
                {"username": reg.username, "password": reg.password, "email": reg.email}).then((res)=>{
                    try {
                        if(res.data.status === "User has successfully been created") {
                            Auth.setAuth(res.data.token);
                            this.props.history.push("/home");
                        } else {
                          throw("Login not successful");
                        }
                    } catch(e) {
                        console.log(e);
                        alert("There was a problem registering you.");
                    }
                    this.props.history.push("/home");
                }).catch((er) => {
                  try{
                    if(er.response.data.status){
                      alert(er.response.data.status);
                    } else {
                      throw("Woops!! Invalid response from server.");
                    }

                  } catch(e) {
                    alert(er);
                  }
                });
            } else {
                alert("Username, password, or email field is blank.")
            }
        } else {
            alert("Passwords are not the same.");
        }
    }
    render() {

        return (
            <div>
            <br/>
                <Jumbotron>
                <Row>
                <img className= "mx-auto" src="CapSoulLogo.png" alt="CapSoul" style={{height: 150}} />
                </Row>
                <Row>
                <h1 className="mx-auto">Welcome to CapSoul!</h1>
                </Row>
                <hr className="my-2" />
                <p className="text-center">A new kind of social media site for storing and sharing the memories that matter with the people who matter</p>
                </Jumbotron>


                <CardDeck>
                  <Card body className="text-center">
                  <Form onSubmit={this.login}>
                      <h2>Login</h2>
                      <FormGroup row>
                        <Col sm={12}>
                          <Input type="text" name="username" placeholder="Username" value={this.state.login.username} onChange={this.handleLoginChange}/>
                        </Col>
                      </FormGroup>

                      <FormGroup row>
                      <Col sm={12}>
                        <Input type="password" name="password" placeholder="Password" value={this.state.login.password} onChange={this.handleLoginChange}/>
                      </Col>
                      </FormGroup>
                      <br/>
                      <br/>
                      <br/>
                      <input type="submit" value="Login" className="btn btn-primary"/>
                  </Form>
                  </Card>


                  <Card body className="text-center">
                  <Form onSubmit={this.register}>
                      <h2>Register</h2>
                      <FormGroup row>
                        <Col sm={12}>
                          <Input type ="email" name="email" placeholder="Email" value={this.state.register.email} onChange={this.handleRegisterChange} />
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col sm={12}>
                          <Input type="text" name="username" placeholder="Username" value={this.state.register.username} onChange={this.handleRegisterChange} />
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col sm={12}>
                          <Input type ="password" name="password" placeholder="Password" value={this.state.register.password} onChange={this.handleRegisterChange} />
                        </Col>
                      </FormGroup>
                      <FormGroup row>
                        <Col sm={12}>
                          <Input type ="password" name="password1" placeholder="Confirm Password" value={this.state.register.password1} onChange={this.handleRegisterChange} />
                        </Col>
                      </FormGroup>
                      <br/>
                      <input type="submit" value="Register" className="btn btn-primary"/>
                  </Form>
                  </Card>
                </CardDeck>
            </div>
        )
    }
}
