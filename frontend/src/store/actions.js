import * as types from './mutation-types'
import * as api from '../api'

export const deleteContact = ({ commit }, pk) => {
    return api.deleteContact(pk).then(response => {
        commit(types.DELETE_CONTACT, { pk: pk })
    })
}

export const updateContact = ({ commit }, [pk, data]) => {
    return api.updateContact(pk, data).then(response => {
        commit(types.UPDATE_CONTACT, { contact: response.data })
    })
}
