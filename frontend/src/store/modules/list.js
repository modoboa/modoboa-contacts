import Vue from 'vue'

import * as api from '../../api'
import * as types from '../mutation-types'

// initial state
const state = {
    contacts: []
}

// getters
const getters = {
    contacts: state => state.contacts
}

// actions
const actions = {
    createContact ({ commit }, data) {
        return api.createContact(data).then(response => {
            commit(types.ADD_CONTACT, { contact: response.data })
        })
    },

    getContacts ({ commit }, [query, category]) {
        return api.getContacts(query, category).then(response => {
            commit(types.SET_CONTACTS, { contacts: response.data })
        })
    }
}

// mutations
const mutations = {
    [types.ADD_CONTACT] (state, { contact }) {
        state.contacts.push(contact)
    },

    [types.DELETE_CONTACT] (state, { pk }) {
        state.contacts = state.contacts.filter(function (contact) {
            return contact.pk !== pk
        })
    },

    [types.SET_CONTACTS] (state, { contacts }) {
        state.contacts = contacts
    },

    [types.UPDATE_CONTACT] (state, { contact }) {
        state.contacts.filter(function (item, pos) {
            if (item.pk === contact.pk) {
                Vue.set(state.contacts, pos, contact)
            }
        })
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
