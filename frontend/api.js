import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

var resource = Vue.resource('/api/v1/contacts{/pk}/')

const createContact = (data) => {
    return resource.save(data)
}

const deleteContact = (pk) => {
    return resource.delete({pk: pk})
}

const getContact = (pk) => {
    return resource.get({pk: pk})
}

const getContacts = (query) => {
    var params = (query) ? { search: query } : {}
    return resource.get(params)
}

const updateContact = (pk, data) => {
    return resource.update({pk: pk}, data)
}

export { createContact, deleteContact, getContact, getContacts, updateContact }
