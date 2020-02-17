import chai from 'chai'
import sinonChai from 'sinon-chai'
import sinon from 'sinon'

import Vue from 'vue'

import GetTextPlugin from 'vue-gettext'
import translations from '@/translations.json'

import SearchForm from '@/components/SearchForm.vue'

describe('SearchForm.vue', () => {
    beforeEach(function () {
        GetTextPlugin.installed = false
        chai.use(sinonChai)
        Vue.use(GetTextPlugin, { translations: translations })
    })

    it('should render correct contents', () => {
        const Ctor = Vue.extend(SearchForm)
        const vm = new Ctor().$mount()
        chai.expect(vm.$el).to.be.ok // eslint-disable-line no-unused-expressions
    })

    it('form submit should emit "search" event with query', () => {
        const Ctor = Vue.extend(SearchForm)
        const vm = new Ctor().$mount()
        const spy = sinon.spy()

        vm.$on('search', spy)
        vm.query = 'Test'
        vm.$el.dispatchEvent(new Event('submit'))
        chai.expect(spy).to.have.been.calledWith('Test')
    })
})
