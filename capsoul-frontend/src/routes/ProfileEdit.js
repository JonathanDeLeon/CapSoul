import React from 'react';
import axios from 'axios';

import { SERVER_URL } from '../config';
import { Auth, Image } from '../components/index';
import { Form, FormGroup, Input, Label, Card, Button, Col, Row} from 'reactstrap';

function TopRender() {
    return (
        <div>
            <header>
                <br/>
                <h1>Edit Your Profile</h1>
                <hr />
            </header>
        </div>
    )
}

export class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);
        if(!Auth.isAuth()) {
            this.props.history.replace("/");
        }

        this.state = {user: null, file: null};
        Auth.getUser().then(user =>{
            console.log("user", user)
            let state = this.state;
            state.user = user;
            this.setState(state);
        });
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePhotoChange = this.handlePhotoChange.bind(this);
    }
     handleChange(event) {
         const target = event.target;
         const value = target.type === 'checkbox' ? target.checked : target.value;
         const name = target.name;
         let state = this.state;
         state.user[name] = value;
         this.setState(state);
    }
    handlePhotoChange(event){
        console.log(event.target.files[0]);
        let file = null;
        if(event.target.files.length >= 1) {
            file = event.target.files[0];
        }
        let state = this.state;
        state.file = file;
        this.setState(state);
    }
    handleSubmit(event) {
        event.preventDefault();
        let user = this.state.user;
        let data;
        //Set data to form or to.
        if(this.state.file) {
            // Create form data object with photo.
            data = new FormData();
            const keys = [
                "first_name",
                "last_name",
                "date_of_birth",
                "email",
                "location",
                "phone"
            ];
            for (let i = 0; i < keys.length; i++) {
                data.append(keys[i], user[keys[i]]);
            }
            //Add profile photo to data obj.
            data.append('photo', this.state.file);
        } else {
            data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": user.date_of_birth,
                "email": user.email,
                "location": user.location,
                "phone": user.phone
            };
        }
        // Send form object to server.
        axios.post(SERVER_URL + "/users", data).then((response) => {
            alert("Saved!");
        }).catch((er) => alert(er));
    }
    render() {
        let user = this.state.user;
        if(user) {
            let profileImg = <Image uri={"/users/media/" + this.state.user.username} className="rounded-circle img-fluid"/>;
            let file = this.state.file;
            if(file) {
                profileImg = <img src={URL.createObjectURL(file)} alt="Profile Image" className="rounded-circle img-fluid"/>
            }
          return (
            <div>
                <TopRender/>
                {/* <ProfileEditRender user={this.state.user}/> */}

                {/*this.props.capsules.map((capsule, i)*/}

                <Form onSubmit={this.handleSubmit}>
                    <Row>
                        <Col sm="12" md={{size: 4, offset: 4}}>
                            {profileImg}
                            <Input type="file" name="photo" onChange={this.handlePhotoChange}/>
                        </Col>
                    </Row>
                    <Row>
                      <Col>
                      <FormGroup>
                      <Label for="first_name">First Name</Label>
                          <Input type="text" name="first_name" value={this.state.user.first_name} onChange={this.handleChange} />
                      </FormGroup>
                      </Col>
                      <Col>
                      <FormGroup>
                      <Label for="last_name">Last Name</Label>
                          <Input type="text" name="last_name" value={this.state.user.last_name} onChange={this.handleChange} />
                      </FormGroup>
                      </Col>
                      <Col>
                      <FormGroup>
                      <Label for="date_of_birth">Birthday</Label>
                          <Input type="date" name="date_of_birth" value={this.state.user.date_of_birth} onChange={this.handleChange} />
                      </FormGroup>
                      </Col>
                    </Row>
                    <Row>
                    <Col>
                      <FormGroup>
                      <Label for="email">Email</Label>
                          <Input type="text" name="email" value={this.state.user.email} onChange={this.handleChange} />
                      </FormGroup>
                    </Col>
                    <Col>
                    <FormGroup>
                    <Label for="phone">Phone</Label>
                        <Input type="text" name="phone" value={this.state.user.phone} onChange={this.handleChange} />
                    </FormGroup>
                    </Col>
                    <Col>
                    <FormGroup>
                    <Label for="location">Location</Label>
                        <Input type="text" name="location" value={this.state.user.location} onChange={this.handleChange} />
                    </FormGroup>
                    </Col>
                </Row>





                    <Button color="primary">Save</Button>
                </Form>
            </div>

            )
        } else {
            return (
                <div>
                    <TopRender/>
                    <div>Loading...</div>
                </div>
            )
        }
    }
}
