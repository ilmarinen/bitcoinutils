const initialState = {
    selectedTab: "LOGIN",
    tabStatus: "LOADED",
    addresses: [],
    selectedAddress: null,
    addressTransactions: [],
    session: {
        authenticated: false,
        user: null
    },
    errorMessage: null
}


function rootReducer(state = initialState, action) {
    switch(action.type) {
        case "LOGIN_REQUESTED":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "LOGIN_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "PROFILE", tabStatus: "LOADED", session: {authenticated: true, user: action.user}});
        case "LOGIN_ERROR":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Login failed"});
        case "LOGOUT_SUCCESSFUL":
            return Object.assign({}, state, {selectedTab: "LOGIN", session: {authenticated: false, user: null}});
        case "LOGOUT_FAILED":
            return Object.assign({}, state, {selectedTab: "PROFILE", errorMessage: "Logout failed"})
        case "REQUEST_USER_ADDRESSES":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_USER_ADDRESSES_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED", addresses: action.addresses});
        case "REQUEST_USER_ADDRESSES_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load addresses"});
        case "REQUEST_USER_ADDRESS_TRANSACTIONS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_USER_ADDRESS_TRANSACTIONS_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED", addressTransactions: action.addressTransactions});
        case "REQUEST_USER_ADDRESS_TRANSACTIONS_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load address transactions"});
        case "REQUEST_ADD_USER_ADDRESS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_ADD_USER_ADDRESS_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED"});
        case "REQUEST_ADD_USER_ADDRESS_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load address transactions"});
        case "SELECT_ADDRESS":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedAddress: action.address});
        case "REQUEST_UPDATE_USER_ADDRESS":
            return Object.assign({}, state, {tabStatus: "LOADING"});
        case "REQUEST_UPDATE_USER_ADDRESS_SUCCEEDED":
            return Object.assign({}, state, {tabStatus: "LOADED"});
        case "REQUEST_UPDATE_USER_ADDRESS_FAILED":
            return Object.assign({}, state, {tabStatus: "LOADED", errorMessage: "Failed to load address transactions"});
        case "SELECT_ADDRESS":
            return Object.assign({}, state, {tabStatus: "LOADED", selectedAddress: action.address});
        default:
            return state
    }
}

export default rootReducer;
