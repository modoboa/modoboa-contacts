import assert from 'assert'
import { expect } from 'chai'

import Vue from 'vue'

import PhoneNumberField from '@/components/PhoneNumberField.vue'

describe('PhoneNumberField.vue', () => {
    it('should render correct contents', () => {
        const Ctor = Vue.extend(PhoneNumberField)
        const vm = new Ctor({ propsData: { index: 0, errors: {}, phone: {} } }).$mount()
        expect(vm.$el).to.be.ok // eslint-disable-line no-unused-expressions
    })

    it('should render correct content with data', () => {
        const Ctor = Vue.extend(PhoneNumberField)
        const vm = new Ctor({
            propsData: {
                index: 0, errors: {}, phone: { number: '0123456789', type: 'cellular' }
            }
        }).$mount()
        expect(vm.$el).to.be.ok // eslint-disable-line no-unused-expressions
        assert.equal(vm.phone.number, '0123456789')
    })
})
