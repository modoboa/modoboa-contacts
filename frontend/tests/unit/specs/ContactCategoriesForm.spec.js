import Vue from 'vue'
import Vuex from 'vuex'
import GetTextPlugin from 'vue-gettext'
import translations from '@/translations.json'

import ContactCategoriesForm from '@/components/ContactCategoriesForm.vue'
import categories from '@/store/modules/categories'

describe('ContactCategoriesForm.vue', () => {
    let state
    let store

    beforeEach(() => {
        const actionsInjector = require('inject-loader!@/store/actions')
        const actions = actionsInjector({
            '../api': {
                updateContact (pk, data) {
                    return new Promise((resolve, reject) => {
                        const contact = {
                            'first_name': 'Homer',
                            'last_name': 'Simpson',
                            emails: [{
                                address: 'homer@simpson.com',
                                type: 'home'
                            }],
                            categories: [1, 2]
                        }
                        return resolve(contact)
                    })
                }
            }
        })
        GetTextPlugin.installed = false
        Vue.use(GetTextPlugin, {translations: translations})

        state = {
            categories: {
                categories: [{
                    pk: 1,
                    name: 'Test 1'
                }, {
                    pk: 2,
                    name: 'Test 2'
                }]
            },
            list: {
                contacts: [{
                    'first_name': 'Homer',
                    'last_name': 'Simpson',
                    emails: [{
                        address: 'homer@simpson.com',
                        type: 'home'
                    }],
                    categories: [1]
                }]
            }
        }

        store = new Vuex.Store({
            state,
            getters: categories.getters,
            actions
        })
    })

    it('should render correct content', () => {
        const Ctor = Vue.extend({ ...ContactCategoriesForm, store })
        const vm = new Ctor({ propsData: { index: 0 } }).$mount()
        Vue.nextTick().then(() => {
            expect(vm.checkedCategories).to.deep.equal([1])
            const input = vm.$el.querySelectorAll('input[type=checkbox]')[0]
            expect(input.value).to.equal(1)
        })
    })

    it('should update contact categories', () => {
        const Ctor = Vue.extend({ ...ContactCategoriesForm, store })
        const vm = new Ctor({ propsData: { index: 0 } }).$mount()

        vm.checkedCategories = [1, 2]
        const form = vm.$el.querySelector('#categoriesForm')
        form.dispatchEvent(new Event('submit'))
        Vue.nextTick().then(() => {
            expect(state.contacts[0].categories).equal.deep.to([1, 2])
        })
    })
})

