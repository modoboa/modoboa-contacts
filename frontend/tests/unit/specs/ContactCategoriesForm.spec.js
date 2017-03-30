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
            getters: categories.getters
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
})

