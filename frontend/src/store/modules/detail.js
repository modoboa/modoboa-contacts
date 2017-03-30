import * as api from '../../api'
import * as types from '../mutation-types'

// initial state
const state = {
    contact: []
}

// getters
const getters = {
    contact: state => state.contact
}

// actions
const actions = {
    getContact ({ commit }, pk) {
        return api.getContact(pk).then(response => {
            commit(types.SET_CONTACT, { contact: response.data })
        })
    }
}

// mutations
const mutations = {
    [types.SET_CONTACT] (state, { contact }) {
        state.contact = contact
    },

    [types.DELETE_CONTACT] (state, { contact }) {
        state.contact = {}
    },

    [types.UPDATE_CONTACT] (state, { contact }) {
        state.contact = contact
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
