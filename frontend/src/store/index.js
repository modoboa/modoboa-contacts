import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions'
import categories from './modules/categories'
import detail from './modules/detail'
import list from './modules/list'

Vue.use(Vuex)

export default new Vuex.Store({
    actions,
    modules: {
        categories,
        detail,
        list
    },
    strict: process.env.NODE_ENV !== 'production'
})
