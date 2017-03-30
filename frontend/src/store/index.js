import Vue from 'vue'
import Vuex from 'vuex'

import * as actions from './actions'
import categories from './modules/categories'
import detail from './modules/detail'
import list from './modules/list'

Vue.use(Vuex)

const options = {
    actions,
    modules: {
        categories,
        detail,
        list
    },
    strict: process.env.NODE_ENV !== 'production'
}

export default new Vuex.Store(options)
export { options }
