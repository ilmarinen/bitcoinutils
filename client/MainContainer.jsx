import React, { Component } from "react";
import ReactDOM from "react-dom";
import LoginForm from "./LoginForm.jsx";
import UserProfile from "./UserProfile.jsx";
import {makePostCall, makeGetCall} from "./ajax";
import { bindActionCreators } from "redux";
import { connect } from 'react-redux';
import {
  loginRequested,
  loginSuccessful,
  loginFailed,
  doLogin,
  checkAuthenticated,
  doLogout,
  getUserAddresses,
  getUserAddressTransactions,
  addUserAddress,
  selectAddress,
  updateUserAddress
} from './actions.js';


function Container({
  selectedTab,
  session,
  restaurants,
  ownerRestaurants,
  orders,
  unplacedOrders,
  addresses,
  selectedAddress,
  addressTransactions,
  restaurantOrders,
  checkAuthenticated,
  doLogin,
  doLogout,
  getUserAddresses,
  getUserAddressTransactions,
  addUserAddress,
  updateUserAddress}) {
    let formComponent;

    if (!session.authenticated) {
      checkAuthenticated();
    }

    if (session.authenticated) {
      formComponent = <UserProfile
                        user={session.user}
                        addresses={addresses}
                        selectedAddress={selectedAddress}
                        addressTransactions={addressTransactions}
                        logoutHandler={doLogout}
                        reloadProfile={checkAuthenticated}
                        getUserAddresses={getUserAddresses}
                        getUserAddressTransactions={getUserAddressTransactions}
                        addUserAddress={addUserAddress}
                        updateUserAddress={updateUserAddress}
                      />;
    } else {
      formComponent = <LoginForm loginHandler={doLogin} />;
    }

    return (
      <div className="container">
          <div className="row">
              <div className="col-lg-8">
                  {formComponent}
              </div>
          </div>
      </div>
    );
}

function mapStateToProps (state) {
  return {
    selectedTab: state.selectedTab,
    session: state.session,
    restaurants: state.restaurants,
    ownerRestaurants: state.ownerRestaurants,
    orders: state.orders,
    restaurantOrders: state.restaurantOrders,
    unplacedOrders: state.unplacedOrders,
    addresses: state.addresses,
    selectedAddress: state.selectedAddress,
    addressTransactions: state.addressTransactions
  };
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators({
    doLogin: doLogin,
    checkAuthenticated: checkAuthenticated,
    doLogout: doLogout,
    getUserAddresses: getUserAddresses,
    getUserAddressTransactions: getUserAddressTransactions,
    addUserAddress: addUserAddress,
    updateUserAddress: updateUserAddress
  }, dispatch);
 }

const MainContainer = connect(mapStateToProps, mapDispatchToProps)(Container)

export default MainContainer;
