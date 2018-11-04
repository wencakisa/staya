export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn
  },

  loggedInUser(state) {
    return state.auth.user
  },
  
  isResident(state) {
    if (getters.loggedInUser(state)) {
      return state.auth.user.is_resident
    }
  }
}

export const mutations = {
  becomeResident(state) {
    state.auth.user.is_resident = true
  }
}
