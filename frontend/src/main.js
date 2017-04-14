import Vue from 'vue'
import VueRouter from 'vue-router'

import Cookies from 'js-cookie'
import moment from 'moment'
import GetTextPlugin from 'vue-gettext'

import store from './store'
import App from './App.vue'
import translations from './translations.json'
import ContactDetail from './components/ContactDetail.vue'
import ContactList from './components/ContactList.vue'

Vue.use(GetTextPlugin, {
    availableLanguages: {
        en: 'English',
        fr: 'Français'
    },
    translations: translations
})
Vue.use(VueRouter)

Vue.filter('formatDate', (value) => {
    if (value) {
        return moment(String(value)).format('MM/DD/YYYY')
    }
})

let csrftoken = Cookies.get('csrftoken')
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken

const routes = [
    { path: '/', name: 'contact-list', component: ContactList },
    { path: '/:pk(\\d+)', name: 'contact-detail', component: ContactDetail },
    { path: '/:category(\\w+)', name: 'contact-list-filtered', component: ContactList }
]

export var router = new VueRouter({
    routes,
    linkActiveClass: 'active'
})

// eslint-disable-next-line no-new
new Vue({
    el: '#app',
    render: h => h(App),
    router,
    store
})

/* global userLang */
Vue.config.language = userLang
