import Vue from 'vue'

import * as api from '../../api'
import * as types from '../mutation-types'

// initial state
const state = {
    categories: []
}

// getters
const getters = {
    categories: state => state.categories
}

// actions
const actions = {
    createCategory ({ commit }, data) {
        return api.createCategory(data).then(response => {
            commit(types.ADD_CATEGORY, { category: response.data })
        })
    },

    getCategories ({ commit }) {
        return api.getCategories().then(response => {
            commit(types.SET_CATEGORIES, { categories: response.data })
        })
    },

    updateCategory ({ commit }, data) {
        return api.updateCategory(data.pk, data).then(response => {
            commit(types.UPDATE_CATEGORY, { category: response.data })
        })
    },

    deleteCategory ({ commit }, data) {
        return api.deleteCategory(data.pk).then(response => {
            commit(types.DELETE_CATEGORY, { pk: data.pk })
        })
    }
}

// mutations
const mutations = {
    [types.ADD_CATEGORY] (state, { category }) {
        state.categories.push(category)
    },

    [types.SET_CATEGORIES] (state, { categories }) {
        state.categories = categories
    },

    [types.UPDATE_CATEGORY] (state, { category }) {
        state.categories.filter(function (item, pos) {
            if (item.pk === category.pk) {
                Vue.set(state.categories, pos, category)
            }
        })
    },

    [types.DELETE_CATEGORY] (state, { pk }) {
        state.categories = state.categories.filter(function (category) {
            return category.pk !== pk
        })
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
