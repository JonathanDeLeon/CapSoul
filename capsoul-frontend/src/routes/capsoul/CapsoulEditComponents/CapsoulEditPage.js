import React, { Component } from 'react';
import axios from 'axios';
import { Link, Redirect } from 'react-router-dom';

// import { Menu } from '../../../components/index';
import { SERVER_URL } from '../../../config';
import { Auth, UserListComponent } from '../../../components/index';

import { LetterComponent } from './LetterComponent';
import { CommentComponent } from './CommentComponent';
import { MediaComponent } from './MediaComponent';
// import {  conf} from '../../../components/api';

import { Form, FormGroup, Input, Label, Card, Button, Col, Row, FormText} from 'reactstrap';

function TopRender() {
    return (
        <div>
            <header>
                <br/>
                <h1> Edit CapSoul  </h1>
                <hr className="my-2" />
            </header>
        </div>
    )
}

// TODO:0 Add editing recipients and contributors.
export class CapsoulEditPage extends Component {
    constructor(props) {
        super(props);
        if(!Auth.isAuth()) {
            this.props.history.replace("/");
        }
        this.state = {"capsule":null,"comment": ""};
        this.fetchCapsoul();

        this.fetchCapsoul = this.fetchCapsoul.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCommentChange = this.handleCommentChange.bind(this);
        this.postComment = this.postComment.bind(this);
        this.postLetter = this.postLetter.bind(this);
        this.mediaChange = this.mediaChange.bind(this);
        this.handleContribChange = this.handleContribChange.bind(this);
        this.handleRecipChange = this.handleRecipChange.bind(this);
        this.removeCapsule = this.removeCapsule.bind(this);
    }
    fetchCapsoul() {
        axios.get(SERVER_URL + "/capsules/" + this.props.match.params.cid).then(response =>{
          this.setState({ "capsule": response.data });
        }).catch((error) => alert(error));
    }
    handleChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        let state = this.state;
        state.capsule[name] = value;
        this.setState(state);
    }
    handleSubmit(event) {
        event.preventDefault();
        let capsule = this.state.capsule;
        axios.post(SERVER_URL + '/capsules/' + this.state.capsule.cid, {
            "unlocks_at": capsule.unlocks_at,
            "owner": capsule.owner_id,
            "contributors": capsule.contributors,
            "recipients": capsule.recipients,
            "title": capsule.title,
            "description": capsule.description
        }).then((response) => {
            alert("Saved!");
        }).catch((er) => alert(er));

    }
    handleCommentChange(event) {
        const val = event.target.value;
        let state = this.state;
        state.comment = val;
        this.setState(state);
    }

    //Callbacks for UserListComponent
    handleRecipChange(recipients) {
        let state = this.state;
        state.capsule.recipients = recipients;
        this.setState(state);
    }
    handleContribChange(contributors) {
        let state = this.state;
        state.capsule.contributors = contributors;
        this.setState(state);
    }

    postComment(event) {
        event.preventDefault();
        axios.post(SERVER_URL + "/capsules/" + this.props.match.params.cid + "/comments", {
            "text": this.state.comment
        }).then((response) => {
            // TODO: Make this actually work. For some reason it doesn't.
            let state = this.state;
            state.comment = "";
            this.setState(state);
            this.fetchCapsoul();
        }).catch((er) => alert(er))
    }
    postLetter() {
        let title = prompt("Letter Title", "");
        let text = prompt("Letter Message", "");
        if(title && text) {
            axios.post(SERVER_URL + "/capsules/" + this.props.match.params.cid + "/letters", {
                "title": title,
                "text": text
            }).then((response) => {
                console.log(response);
            }).catch((er) => {alert(er)});
            this.fetchCapsoul();
        } else {
            alert("Your letter is blank.");
        }
    }
    mediaChange(event) {
        if(event.target.files.length >= 1) {
            let file = event.target.files[0];
            let data = new FormData();
            data.append('file', file, "name");
            axios.post(SERVER_URL + "/capsules/" + this.props.match.params.cid + "/media", data).then(
                (res) => {
                    let state = this.state;
                    try {
                        state.capsule.media.push(res.data.mid);
                        this.setState(state);
                    } catch(e) {
                        alert(e);
                    }
                }
            ).catch((er) => alert(er))
        }
    }
    removeCapsule() {
      // let confirm = confirm("Are you sure you want to delete this CapSoul?");
      if (window.confirm("Are you sure you want to remove this CapSoul?")) {
        axios.delete(SERVER_URL + "/capsules/" + this.props.match.params.cid).then((res) => {
          try {
            if (res.data.status === "capsule deleted") {
              this.props.history.push("/home");
            }
          } catch (e) {
            if (res && res.data && res.data.status) {
              alert(res.data.status);
            } else {
              alert("We couldn't delete that capsule for you right now.");
            }
          }
        });
      }
    }
    render() {
      let capsule = this.state.capsule;
        if(capsule) {

          var displayDateTime = new Date(capsule.unlocks_at.toLocaleString());
          var newDate = new Date(displayDateTime.getTime()-displayDateTime.getTimezoneOffset()*60*1000).toISOString();

          const letters = capsule.letters.map((letter, i )=> {
            return(
              <LetterComponent key={letter} cid={capsule.cid} lid={letter} reload={this.fetchCapsoul}/>
            )
          });
          const media = capsule.media.map((media, i) => {
            return(
                <MediaComponent key={media} cid={capsule.cid} mid={media} reload={this.fetchCapsoul}/>
            )
          });
          const comments = capsule.comments.map((comment, i) => {
            return(
              <CommentComponent key={comment.comid} comment={comment}/>
            )
          });
          return (
              <div>
                  <TopRender/>

                  <Form onSubmit={this.handleSubmit}>

                  <Row>
                      <Col>
                        <FormGroup>
                          <Label for="title">Title</Label>
                            <Input type="text" name="title" placeholder="with a placeholder" value={capsule.title} onChange={this.handleChange}/>
                        </FormGroup>
                      </Col>
                      <Col>
                        <FormGroup>
                          <Label for="unlocks_at">Unlock Date:</Label>
                            <Input type="datetime-local" name="unlocks_at" value={newDate.replace("Z","")} onChange={this.handleChange}/>
                        </FormGroup>
                      </Col>
                  </Row>
                  <Row>
                      <Col>
                        <FormGroup>
                          <Label for="contributors">Contributor(s)</Label>
                          <UserListComponent init={capsule.contributors} disabled={capsule.recipients} callback={this.handleContribChange}/>
                        </FormGroup>
                      </Col>
                      <Col>
                        <FormGroup>
                          <Label for="recipients">Recipient(s)</Label>
                          <UserListComponent init={capsule.recipients} disabled={capsule.contributors} callback={this.handleRecipChange}/>
                        </FormGroup>
                      </Col>
                  </Row>

                  <hr className="my-2" />

                  <Row>
                    <Col>
                    <FormGroup>
                      <Label for="description">Description</Label>
                        <Input type="textarea" name="description" value={capsule.description} onChange={this.handleChange}/>
                    </FormGroup>
                    </Col>
                    </Row>
                  <Button color="primary">Save</Button>
                  <Button className="btn btn-danger btn-sm" onClick={this.removeCapsule}>Delete</Button>
                  </Form>
                  <hr className="my-2" />

                  <h2>Letters</h2>
                  <div className="card-columns">
                      {letters}
                  </div>
                  <Button color="primary" onClick={this.postLetter}>Add a letter</Button>
                  <hr className="my-2" />
                  <h2>Media</h2>
                  <div className="card-columns">
                      {media}
                  </div>
                  <br/>
                  <p>Add Media:</p>
                  <input type="file" label="Upload" accept="image/*" className="form-control-file" onChange={this.mediaChange}/>
                  <hr className="my-2" />

                  <h2>Comments</h2>
                  {comments}
                  <Form onSubmit={this.postComment}>
                  <FormGroup>
                    <Label for="comment">Comment</Label>
                      <Input type="text" name="comment" placeholder="Leave a comment here!" value={this.state.comment} onChange={this.handleCommentChange}/>
                  </FormGroup>
                      <Button color='primary'>Send</Button>
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
