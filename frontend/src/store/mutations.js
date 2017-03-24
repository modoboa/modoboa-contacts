import Vue from 'vue'
import * as types from './mutation-types'

export const state = {
    contacts: []
}

export const mutations = {
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
