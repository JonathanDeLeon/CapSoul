import React, { Component } from 'react';
import axios from 'axios';
import { Form, FormGroup, Input, Label, Card, Button, Col, Row} from 'reactstrap';

import { Auth, UserListComponent } from '../components/index';
import { SERVER_URL } from '../config';

// TODO:10 Allow for multiple contributors/recipients.
export class Create extends Component {
    constructor(props) {
        super(props);
        if(!Auth.isAuth()) {
            this.props.history.replace("/");
        }
        this.state= {"title":"", "date":"", "contributors":[], "recipients":[]};

        //Link the `this` keyword to the functions that are part of the component.
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleContribChange = this.handleContribChange.bind(this);
        this.handleRecipChange = this.handleRecipChange.bind(this);
    }

    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        let state = this.state;
        state[name] = value;
        this.setState(state);
    }



    handleSubmit(event) {
        event.preventDefault();
        let state = this.state;
        let fixdate = new Date(this.state.date).toISOString();
        let nowDate = new Date();
        let setDate = new Date(this.state.date);
        if(setDate > nowDate){
          axios.post(SERVER_URL + "/capsules", {
              "title": state.title,
              "unlocks_at": fixdate,
              "contributors": state.contributors,
              "recipients": state.recipients,
              "description": ""
          }).then((response) => {
              if (response && response.data && response.data.cid) {
                  this.props.history.push("/capsoul/edit/" + response.data.cid);
                  alert("Saved!");
              } else {
                  alert("There was a problem.");
              }
          }).catch((er) => alert(er));
        }
        else{
          alert("The date you've picked is in the past!");
        }

    }
    //Calbacks for the UserListComponents.
    handleContribChange(contributors) {
        let state = this.state;
        state.contributors = contributors;
        this.setState(state);
    }
    handleRecipChange(recipients) {
        let state = this.state;
        state.recipients = recipients;
        this.setState(state);
    }
    render() {
        return (
            <div>
                <header>
                    <br/>
                    <h1>Create a CapSoul</h1>
                    <hr />
                </header>
                <Form onSubmit={this.handleSubmit}>
                <Row>
                  <Col>
                  <FormGroup>
                    <Label for="title">Event Name</Label>
                      <Input type="text" name="title" value={this.state.title} onChange={this.handleChange} />
                  </FormGroup>
                  </Col>
                  <Col>
                  <FormGroup>
                    <Label for="date">Unlock Date</Label>
                    <Input type="datetime-local" name="date" value={this.state.date} onChange={this.handleChange}/>
                  </FormGroup>
                  </Col>
                </Row>
                <Row>
                  <Col>
                    <FormGroup>
                    <Label for="contributors">Contributor(s):</Label>
                    <UserListComponent disabled={this.state.recipients} callback={this.handleContribChange}/>
                    </FormGroup>
                  </Col>
                  <Col>
                    <FormGroup>
                      <Label for="recipients">Recipient:</Label>
                      <UserListComponent disabled={this.state.contributors} callback={this.handleRecipChange}/>
                    </FormGroup>
                  </Col>
                </Row>
                <Button color="primary">Create</Button>
                </Form>
            </div>
        )
    }
}
