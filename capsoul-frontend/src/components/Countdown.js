import React, { Component } from 'react';

export class Countdown extends Component {
  constructor(props) {
      super(props);
      this.timer = 0;
      this.state = {seconds: this.dateToSeconds(props.time), time: 0};
	    this.countDown = this.countDown.bind(this);

  }

  secondsToTime(secs) {
      let years = Math.floor(secs/ (60*60*24*365));

      let divisor_for_days = secs % (60*60*24*365);
      let days = Math.floor(divisor_for_days / (60*60*24));

      let divisor_for_hours = secs % (60*60*24);
      let hours = Math.floor(divisor_for_hours / (60 * 60));

      let divisor_for_minutes = secs % (60 * 60);
      let minutes = Math.floor(divisor_for_minutes / 60);

      let divisor_for_seconds = divisor_for_minutes % 60;
      let seconds = Math.ceil(divisor_for_seconds);

      let obj = {
          "y": years,
          "d": days,
          "h": hours,
          "m": minutes,
          "s": seconds
      };
      return obj;
  }
  componentDidMount() {
    this.setState({time: this.secondsToTime(this.state.seconds)});
    this.startTimer(this.state.seconds);
    //console.log("Mounted!");
  }

  startTimer() {
      if (this.timer == 0) {
          this.timer = setInterval(this.countDown, 1000);
          //console.log("Timer Started!");
      }
      else {
        //console.log("Timer could not start.");
      }
  }

  dateToSeconds(h) {
      h = new Date(h)
      let seconds = h.getTime() / 1000;
      let dtime = new Date()
      let sec2 = Math.floor(dtime.getTime() / 1000);
      let secDelta = seconds - sec2;

      return secDelta;
  }

  countDown() {
      // Remove one second, set state so a re-render happens.

      this.setState({seconds: (this.state.seconds-1)});
      this.setState({time: (this.secondsToTime(this.state.seconds))});

      // Check if we're at zero.
      if (this.state.seconds <= 0) {
          clearInterval(this.timer);
          this.setState({seconds: 0});
          this.setState({time: (this.secondsToTime(this.state.seconds))});
      }
  }

  render()  {
    //console.log(this.state.time);
    var renderYear = <span>Y:{this.state.time.y}</span>;
    if(this.state.time.y == 0){
      renderYear = "";
    }
    var renderDay = <span>D:{this.state.time.d}</span>;
    if(this.state.time.d == 0){
      renderDay = "";
    }
    var renderHour = <span>H: {this.state.time.h}</span>;
    if(this.state.time.h == 0){
      renderHour = "";
    }
    var renderMinute = <span>M: {this.state.time.m}</span>;
    var renderSecond = <span>S: {this.state.time.s}</span>;
    return(
    <div>
        Countdown: <br/>
        {renderYear} {renderDay} {renderHour} {renderMinute} {renderSecond}
    </div>
    )
  }
}
