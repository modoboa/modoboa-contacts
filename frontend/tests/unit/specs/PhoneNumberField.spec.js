import assert from 'assert'

import Vue from 'vue'

import PhoneNumberField from '@/components/PhoneNumberField.vue'

describe('PhoneNumberField.vue', () => {
    it('should render correct contents', () => {
        const Ctor = Vue.extend(PhoneNumberField)
        const vm = new Ctor({ propsData: { index: 0, errors: {} } }).$mount()
        expect(vm.$el).to.be.ok
    })

    it('should render correct content with data', () => {
        const Ctor = Vue.extend(PhoneNumberField)
        const vm = new Ctor({
            propsData: {
                index: 0, errors: {}, number: '0123456789', 'type': 'cellular'
            }
        }).$mount()
        expect(vm.$el).to.be.ok
        assert.equal(vm.phoneNumber.number, '0123456789')

        let spy = sinon.spy()
        vm.$on('updated', spy)
        vm.phoneNumber.type = 'pager'
        Vue.nextTick(() => {
            expect(spy).to.have.been.calledWith({ number: '0123456789', type: 'pager' })
        })
    })
})
