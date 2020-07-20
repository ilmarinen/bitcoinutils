import React, { Component } from "react";
import ReactDOM from "react-dom";
import {makePostCall, makeGetCall, makePutCall, makeDeleteCall} from "./ajax";


class UserProfile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: this.props.user,
      editUser: false,
      editUserId: this.props.user.id,
      editUserUsername: this.props.user.username,
      editUserFirstName: this.props.user.firstname,
      editUserLastName: this.props.user.lastname,
      addresses: this.props.addresses,
      newAddress: "",
      selectedAddress: this.props.selectedAddress,
      addressTransactions: this.props.addressTransactions
    };

  this.updateUser = this.updateUser.bind(this);
  this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
  this.handleLastNameChange = this.handleLastNameChange.bind(this);
  this.handleNewAddressChange = this.handleNewAddressChange.bind(this);
  this.handleSelectAddress = this.handleSelectAddress.bind(this);
  this.handleAddUserAddress = this.handleAddUserAddress.bind(this);
  this.logout = this.logout.bind(this);
  this.reload = this.reload.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      user: nextProps.user,
      editUser: false,
      editUserId: nextProps.user.id,
      editUserUsername: nextProps.user.username,
      editUserFirstName: nextProps.user.firstName,
      editUserLastName: nextProps.user.lastName,
      addresses: nextProps.addresses,
      selectedAddress: nextProps.selectedAddress,
      addressTransactions: nextProps.addressTransactions
    });
  }

  componentDidMount() {
    this.props.getUserAddresses(this.state.user.id);
  }

  handleFirstNameChange(evt) {
    this.setState({
      editUserFirstName: evt.target.value,
    });
  }

  handleLastNameChange(evt) {
    this.setState({
      editUserLastName: evt.target.value
    });
  }

  handleNewAddressChange(evt) {
    this.setState({
      newAddress: evt.target.value
    });
  }

  handleSelectAddress(address) {
    return () => {
      this.props.getUserAddressTransactions(this.props.user.id, address);
    }
  }

  handleAddUserAddress(evt) {
    this.props.addUserAddress(this.props.user.id, this.state.newAddress);
    this.setState({
      newAddress: ""
    });
  }

  handleUpdateUserAddress(address) {
    return () => {
      this.props.updateUserAddress(this.props.user.id, address);
    }
  }

  updateUser() {
    this.props.updateUser(this.state.editUserId, this.state.editUserFirstName, this.state.editUserLastName)
  }

  logout(e) {
    e.stopPropagation();
    this.props.logoutHandler();
  }

  reload() {
    this.props.reloadProfile();
  }

  render() {
    var _this = this;
    let transactionsComponent;

    var cardStyle = {
      "maxWidth": "18rem"
    };

    const profileImage = (this.props.user.profile_filename != "" && this.props.user.profile_filename != null)?("uploads/" + this.props.user.profile_filename):"static/profile.png";

    if (this.state.selectedAddress) {
      transactionsComponent = (
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3">
          <div className="card-header">Transactions for {this.state.selectedAddress.address}</div>
          <div className="card-body text-primary">
            {this.state.addressTransactions.map(addressTransaction => {
              return (<div>
                <div>{addressTransaction.hash}</div>
              </div>);
            })}
          </div>
          </div>
        </div>
      );
    }

    return (
      <div className="container">
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3">
            <div className="card-header">{this.state.user.username}</div>
            <div className="card-body text-primary">
              <h6 className="card-text">{`${this.state.user.firstname} ${this.state.user.lastname}`}</h6>
              <div className="card-body text-primary">
                <input type="text" className="form-control form-field" onChange={this.handleNewAddressChange} value={this.state.newAddress} />
                 <a href="#" className="btn btn-primary" onClick={this.handleAddUserAddress}>Add Address</a>
              </div>
              <a href="#" className="btn btn-primary" onClick={this.logout}>Logout</a>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="card info-card bg-border-secondary mb-3">
          <div className="card-header">Addresses</div>
          <div className="card-body text-primary">
            {this.state.addresses.map(address => {
              return (<div onClick={this.handleSelectAddress(address)}>
                <div>{address.address}</div>
                <div>Final Balance: {address.final_balance}</div>
                <a href="#" className="btn btn-primary" onClick={this.handleUpdateUserAddress(address)}>Update Transactions</a>
              </div>);
            })}
          </div>
          </div>
        </div>
        {transactionsComponent}
      </div>
    );
  }
}
export default UserProfile;
