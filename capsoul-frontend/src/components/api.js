import axios from 'axios';
import { SERVER_URL } from '../config';

class Authentication {
  constructor() {
    this.user = null;
    if(this.isAuth()){
      axios.defaults.headers.common['Authorization'] = "Token " + localStorage.token;
      axios.get(SERVER_URL + "/verify/").then((res) => {
        try{
          if(res.data.status === "User has been successfully created" && res.data.user) {
            this.user = res.data.user[0].fields;
            this.user.username = res.data.user[0].pk;
          }
        } catch(e) {
          this.user = null;
        }
      }).catch((er) => {
        console.log("get User failed");
        this.removeAuth();
        window.location.reload();

      } );
    }
  }
  setAuth(token) {
    if(!token) {
      throw("Token must be defined.");
    }
    window.localStorage.setItem('token', token);
    axios.defaults.headers.common['Authorization'] = "Token " + token;
    // this.getUser();
  }
  removeAuth() {
    let token = window.localStorage.getItem("token");
    window.localStorage.removeItem("token");
  }
  isAuth() {
    return Boolean(localStorage.token);
  }
  getUser() {
    if(this.user) {
      return new Promise((resolve, reject) => {
        resolve(this.user);
      });
    } else {
      return axios.get(SERVER_URL + "/verify/").then((res) => {
        // TODO: Check if the token we have is invalid.
        let user = res.data.user[0].fields;
        user.username = res.data.user[0].pk;
        return user;
      });
    }
  }
}

export let Auth = new Authentication();
