import * as types from './mutation-types'
import * as api from '../api'

export const createContact = ({ commit }, data) => {
    return api.createContact(data).then(response => {
        commit(types.ADD_CONTACT, { contact: response.data })
    })
}

export const deleteContact = ({ commit }, pk) => {
    return api.deleteContact(pk).then(response => {
        commit(types.DELETE_CONTACT, { pk: pk })
    })
}

export const getContacts = ({ commit }, query) => {
    return api.getContacts(query).then(response => {
        commit(types.SET_CONTACTS, { contacts: response.data })
    })
}

export const updateContact = ({ commit }, [ pk, data ]) => {
    return api.updateContact(pk, data).then(response => {
        commit(types.UPDATE_CONTACT, { contact: response.data })
    })
}
