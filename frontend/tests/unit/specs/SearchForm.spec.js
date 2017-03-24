import Vue from 'vue'

import GetTextPlugin from 'vue-gettext'
import translations from '@/translations.json'

import SearchForm from '@/components/SearchForm.vue'

describe('SearchForm.vue', () => {
    beforeEach(function () {
        GetTextPlugin.installed = false
        Vue.use(GetTextPlugin, {translations: translations})
    })

    it('should render correct contents', () => {
        const Ctor = Vue.extend(SearchForm)
        const vm = new Ctor().$mount()
        expect(vm.$el).to.be.ok
    })

    it('form submit should emit "search" event with query', () => {
        const Ctor = Vue.extend(SearchForm)
        const vm = new Ctor().$mount()
        let spy = sinon.spy()

        vm.$on('search', spy)
        vm.query = 'Test'
        vm.$el.dispatchEvent(new Event('submit'))
        expect(spy).to.have.been.calledWith('Test')
    })
})
