import Vue from 'vue'
import Cookies from 'js-cookie'
import GetTextPlugin from 'vue-gettext'
import VueRouter from 'vue-router'
import store from './store'
import App from './App.vue'
import translations from './translations.json'
import ContactDetail from './components/ContactDetail.vue'
import ContactList from './components/ContactList.vue'

Vue.use(GetTextPlugin, {translations: translations})
Vue.use(VueRouter)

let csrftoken = Cookies.get('csrftoken')
Vue.http.headers.common['X-CSRFTOKEN'] = csrftoken

const routes = [
    { path: '/', name: 'contact-list', component: ContactList },
    { path: '/:category(\\w+)/', name: 'contact-list-filtered', component: ContactList },
    { path: '/:pk(\\d+)/', name: 'contact-detail', component: ContactDetail }
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
