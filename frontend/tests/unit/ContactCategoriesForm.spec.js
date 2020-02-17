import Vue from 'vue'
import Vuex from 'vuex'
import GetTextPlugin from 'vue-gettext'
import translations from '@/translations.json'

import { expect } from 'chai'

import ContactCategoriesForm from '@/components/ContactCategoriesForm.vue'
import categories from '@/store/modules/categories'
import list from '@/store/modules/list'

describe('ContactCategoriesForm.vue', () => {
    let store

    beforeEach(() => {
        const actionsInjector = require('inject-loader!@/store/actions') // eslint-disable-line import/no-webpack-loader-syntax
        const actions = actionsInjector({
            '../api': {
                updateContact (pk, data) {
                    return Promise.resolve({
                        data: {
                            pk: 1,
                            first_name: 'Homer',
                            last_name: 'Simpson',
                            emails: [{
                                address: 'homer@simpson.com',
                                type: 'home'
                            }],
                            categories: [1, 2]
                        }
                    })
                }
            }
        })
        GetTextPlugin.installed = false
        Vue.use(GetTextPlugin, { translations: translations })
        Vue.use(Vuex)
        store = new Vuex.Store({
            actions,
            modules: {
                categories: {
                    state: {
                        categories: [{
                            pk: 1,
                            name: 'Test 1'
                        }, {
                            pk: 2,
                            name: 'Test 2'
                        }]
                    },
                    getters: categories.getters
                },
                list: {
                    mutations: list.mutations,
                    state: {
                        contacts: [{
                            pk: 1,
                            first_name: 'Homer',
                            last_name: 'Simpson',
                            emails: [{
                                address: 'homer@simpson.com',
                                type: 'home'
                            }],
                            categories: [1]
                        }]
                    }
                }
            }
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

    it('should update contact categories', (done) => {
        const Ctor = Vue.extend({ ...ContactCategoriesForm, store })
        const vm = new Ctor({ propsData: { index: 0 } }).$mount()

        vm.checkedCategories = [1, 2]
        const form = vm.$el.querySelector('#categoriesForm')
        form.dispatchEvent(new Event('submit'))
        Vue.nextTick().then(() => {
            expect(store.state.list.contacts[0].categories).to.deep.equal([1, 2])
            done()
        }).catch(done)
    })
})
