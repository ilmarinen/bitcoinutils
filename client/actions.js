import {makePostCall, makeGetCall, makePutCall} from "./ajax";


function loginRequested() {
    return {
        type: "LOGIN_REQUESTED"
    }
}

function loginSuccessful(user) {
    return {
        type: "LOGIN_SUCCESSFUL",
        user: user
    }
}

function loginFailed(error) {
    return {
        type: "LOGIN_FAILED",
        error: error
    }
}

function logoutSuccessful() {
    return {
        type: "LOGOUT_SUCCESSFUL"
    }
}

function logoutFailed(error) {
    return {
        type: "LOGOUT_FAILED",
        error: error
    }
}

function  doLogin(username, password) {
    return function(dispatch) {
        dispatch(loginRequested);
        makePostCall(
          "api/v1/users/authenticated",
          {
            username: username,
            password: password
          }
        ).then(user => dispatch(loginSuccessful(user))
          ).catch(res => dispatch(loginFailed(res)));
    }
}

function doLogout() {
    return function(dispatch) {
        makePostCall("api/v1/users/logout")
          .then(res => {dispatch(logoutSuccessful()), dispatch(selectLogin())})
          .fail(res => dispatch(logoutFailedf(error)));
    }
}

function requestGetUserAddresses() {
    return {
        type: "REQUEST_USER_ADDRESSES"
    }
}

function requestGetUserAddressesSucceeded(addresses) {
    return {
        type: "REQUEST_USER_ADDRESSES_SUCCEEDED",
        addresses: addresses
    }
}

function requestGetUserAddressesFailed(error) {
    return {
        type: "REQUEST_USER_ADDRESSES_FAILED",
        error: error
    }
}

function getUserAddresses(userId) {
    return function(dispatch) {
        dispatch(requestGetUserAddresses);
        makeGetCall("api/v1/users/" + userId + "/addresses")
          .done(addresses => {dispatch(requestGetUserAddressesSucceeded(addresses))})
          .fail(error => dispatch(requestGetUserAddressesFailed(error)));
    }
}

function requestGetUserAddressTransactions() {
    return {
        type: "REQUEST_USER_ADDRESS_TRANSACTIONS"
    }
}

function requestGetUserAddressTransactionsSucceeded(addressTransactions) {
    return {
        type: "REQUEST_USER_ADDRESS_TRANSACTIONS_SUCCEEDED",
        addressTransactions: addressTransactions
    }
}

function requestGetUserAddressTransactionsFailed(error) {
    return {
        type: "REQUEST_USER_ADDRESS_TRANSACTIONS_FAILED",
        error: error
    }
}

function selectAddress(address) {
    console.log(address);
    return {
        type: "SELECT_ADDRESS",
        address: address
    }
}

function getUserAddressTransactions(userId, address) {
    return function(dispatch) {
        dispatch(requestGetUserAddressTransactions);
        makeGetCall("api/v1/users/" + userId + "/addresses/" + address.id + "/transactions")
          .done(addressTransactions => {dispatch(requestGetUserAddressTransactionsSucceeded(addressTransactions)), dispatch(selectAddress(address))})
          .fail(error => dispatch(requestGetUserAddressesFailed(error)));
    }
}

function requestAddUserAddress() {
    return {
        type: "REQUEST_ADD_USER_ADDRESS"
    }
}

function requestAddUserAddressSucceeded(address) {
    return {
        type: "REQUEST_ADD_USER_ADDRESS_SUCCEEDED",
        address: address
    }
}

function requestAddUserAddressFailed(error) {
    return {
        type: "REQUEST_ADD_USER_ADDRESS_FAILED",
        error: error
    }
}

function addUserAddress(userId, address) {
    return function(dispatch) {
        dispatch(requestAddUserAddress);
        makePostCall("api/v1/users/" + userId + "/addresses", {address: address})
          .done(address => {dispatch(requestAddUserAddressSucceeded(address)), dispatch(getUserAddresses(userId))})
          .fail(error => dispatch(requestAddUserAddressFailed(error)));
    }
}

function requestUpdateUserAddress() {
    return {
        type: "REQUEST_UPDATE_USER_ADDRESS"
    }
}

function requestUpdateUserAddressSucceeded(address) {
    return {
        type: "REQUEST_UPDATE_USER_ADDRESS_SUCCEEDED",
        address: address
    }
}

function requestUpdateUserAddressFailed(error) {
    return {
        type: "REQUEST_UPDATE_USER_ADDRESS_FAILED",
        error: error
    }
}

function updateUserAddress(userId, address) {
    return function(dispatch) {
        dispatch(requestUpdateUserAddress);
        makeGetCall("api/v1/users/" + userId + "/addresses/" + address.id + "/get_updates")
          .done(address => {dispatch(requestUpdateUserAddressSucceeded(address)), dispatch(getUserAddresses(userId))})
          .fail(error => dispatch(requestUpdateUserAddressFailed(error)));
    }
}

function checkAuthenticated() {
    return function(dispatch) {
        makeGetCall("api/v1/users/authenticated")
          .done(user => {dispatch(loginSuccessful(user)), dispatch(getUserAddresses(user.id))});
    }
}

export {
    loginRequested,
    loginSuccessful,
    loginFailed,
    doLogin,
    checkAuthenticated,
    doLogout,
    getUserAddresses,
    getUserAddressTransactions,
    addUserAddress,
    updateUserAddress
};
