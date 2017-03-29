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
    }
}

// mutations
const mutations = {
    [types.ADD_CATEGORY] (state, { category }) {
        state.categories.push(category)
    },

    [types.SET_CATEGORIES] (state, { categories }) {
        state.categories = categories
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
