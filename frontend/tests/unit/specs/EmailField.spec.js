import assert from 'assert'

import Vue from 'vue'

import EmailField from '@/components/EmailField.vue'

describe('EmailField.vue', () => {
    it('should render correct contents', () => {
        const Ctor = Vue.extend(EmailField)
        const vm = new Ctor({ propsData: { index: 0, errors: {} } }).$mount()
        expect(vm.$el).to.be.ok
    })

    it('should render correct content with data', done => {
        const Ctor = Vue.extend(EmailField)
        const vm = new Ctor({
            propsData: {
                index: 0, errors: {}, address: 'test@toto.com', 'type': 'home'
            }
        }).$mount()
        expect(vm.$el).to.be.ok
        assert.equal(vm.email.address, 'test@toto.com')
        let spy = sinon.spy()
        vm.$on('updated', spy)
        vm.email.type = 'work'
        Vue.nextTick(() => {
            assert(spy.calledWith({ address: 'test@toto.com', type: 'work' }))
            done()
        })
    })
})
