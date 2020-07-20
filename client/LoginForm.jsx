import React, { Component } from "react";
import ReactDOM from "react-dom";
class LoginForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      errorMessage: ""
    };
    this.loginClick = this.loginClick.bind(this);
    this.handleUsernameChange = this.handleUsernameChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (!!nextProps.errorMessage) {
      this.setState({
        errorMessage: nextProps.errorMessage
      });
    }
  }

  handleUsernameChange(event) {
    this.setState({
      username: event.target.value
    });
  }

  handlePasswordChange(event) {
    this.setState({
      password: event.target.value
    })
  }

  loginClick(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    this.props.loginHandler(this.state.username, this.state.password);
  }

  render() {
    let errorMessage;

    if (this.state.errorMessage) {
      errorMessage = (
        <span className="error text-danger">{this.state.errorMessage}</span>
      );
    } else {
      errorMessage = "";
    }

    return (
      <form>
          {errorMessage}
          <div className="form-group">
              <input type="text" className="form-control" placeholder="Username" defaultValue="" onChange={this.handleUsernameChange} />
          </div>
          <div className="form-group">
              <input type="password" className="form-control" placeholder="Password" defaultValue="" onChange={this.handlePasswordChange} />
          </div>
          <div className="form-group">
              <input type="submit" className="btnSubmit" defaultValue="Login" onClick={this.loginClick} />
          </div>
      </form>
    );
  }
}
export default LoginForm;
