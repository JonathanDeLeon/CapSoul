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


            </header>
        </div>
    )
}

// TODO:0 Add editing recipients and contributors.
export class CapsoulPage extends Component {
    constructor(props) {
        super(props);
        if(!Auth.isAuth()) {
            this.props.history.replace("/");
        }
        this.state = {"capsule":null,"comment": null};
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
        axios.post(SERVER_URL + "/capsules/" + this.props.match.params.cid + "/letters", {
            "title": title,
            "text": text
        }).then((response) => {
            console.log(response);
        }).catch((er) => {alert(er)});
        this.fetchCapsoul();
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


          var contributorPrint = capsule.owner_id;

          for (var i = 0; i < capsule.contributors.length; i++)
          {
              if(i+1==capsule.contributors.length){
                contributorPrint += capsule.contributors[i];
              }
              else{
                contributorPrint += ", " + capsule.contributors[i];
              }
          }

          var recipientPrint = "";

          for (var i = 0; i < capsule.recipients.length; i++)
          {
            if(i+1!=capsule.recipients.length){
              recipientPrint += capsule.recipients[i] + ", ";
            }
            else{
              recipientPrint += capsule.recipients[i];
            }
          }

          var displayDateTime = new Date(capsule.unlocks_at.toLocaleString());
          var printDate = new Date(capsule.unlocks_at).toLocaleString();
          console.log(displayDateTime);
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

                  <Row>
                      <Col className="text-center">
                        <div>
                          <h2>{capsule.title}</h2>
                          <br/>
                        </div>
                      </Col>
                  </Row>

                  <Row className = "text-center">
                      <Col>
                        <div>
                          <h4>Contributors: {contributorPrint}</h4>
                        </div>
                      </Col>
                      <Col>
                        <div>
                          <h4>Recipients: {recipientPrint}</h4>
                        </div>
                      </Col>
                      <Col>
                        <div>
                          <h4>{printDate} </h4>
                        </div>
                      </Col>
                  </Row>

                  <hr className="my-2" />

                  <Row>
                    <Col>
                    <div>
                      <h2 className = "text-center" >Description</h2>
                       <p>{capsule.description}</p>
                    </div>
                    </Col>
                    </Row>
                  <hr className="my-2" />

                  <h2 className="text-center">Letters</h2>
                  <br/>
                  <div className="card-columns">
                      {letters}
                  </div>

                  <hr className="my-2" />

                  <h2 className="text-center">Media</h2>
                  <br/>
                  <div className="card-columns">
                      {media}
                  </div>
                  <br/>


                  <hr className="my-2" />

                  <h2>Comments</h2>
                  {comments}
                  <Form onSubmit={this.postComment}>
                  <FormGroup>
                      <Input type="text" name="comment" placeholder="Leave a comment here!" value={this.comment} onChange={this.handleCommentChange}/>
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
