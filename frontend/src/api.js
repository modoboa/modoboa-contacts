import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

var customAddressBookActions = {
    default: { method: 'GET', url: '/api/v1/address-books/default/' },
    sync: { method: 'GET', url: '/api/v1/address-books/sync_to_cdav/' }
}
var addressBookResource = Vue.resource(
    '/api/v1/address-books{/pk}/', {}, customAddressBookActions)
var categoryResource = Vue.resource('/api/v1/categories{/pk}/')
var contactResource = Vue.resource('/api/v1/contacts{/pk}/')

// address book API
const getDefaultAddressBook = () => {
    return addressBookResource.default()
}

const syncAddressBook = () => {
    return addressBookResource.sync()
}

// categories API
const createCategory = (data) => {
    return categoryResource.save(data)
}

const getCategories = () => {
    return categoryResource.get()
}

const updateCategory = (pk, data) => {
    return categoryResource.update({ pk: pk }, data)
}

const deleteCategory = (pk) => {
    return categoryResource.delete({ pk: pk })
}

// contacts API
const createContact = (data) => {
    return contactResource.save(data)
}

const deleteContact = (pk) => {
    return contactResource.delete({ pk: pk })
}

const getContact = (pk) => {
    return contactResource.get({ pk: pk })
}

const getContacts = (query, category) => {
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
    return contactResource.update({ pk: pk }, data)
}

export {
    getDefaultAddressBook,
    syncAddressBook,

    createCategory,
    getCategories,
    updateCategory,
    deleteCategory,

    createContact,
    deleteContact,
    getContact,
    getContacts,
    updateContact
}
