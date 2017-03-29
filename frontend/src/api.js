import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

var categoryResource = Vue.resource('/api/v1/categories{/pk}/')
var contactResource = Vue.resource('/api/v1/contacts{/pk}/')

// categories API
const createCategory = (data) => {
    return categoryResource.save(data)
}

const getCategories = () => {
    return categoryResource.get()
}

// contacts API
const createContact = (data) => {
    return contactResource.save(data)
}

const deleteContact = (pk) => {
    return contactResource.delete({pk: pk})
}

const getContact = (pk) => {
    return contactResource.get({pk: pk})
}

const getContacts = ({ query, category }) => {
    var params = {}

    if (query !== undefined) {
        params.search = query
    }
    if (category !== undefined) {
        params.category = category
    }
    return contactResource.get(params)
}

const updateContact = (pk, data) => {
    return contactResource.update({pk: pk}, data)
}

export {
    createCategory,
    getCategories,

    createContact,
    deleteContact,
    getContact,
    getContacts,
    updateContact
}
