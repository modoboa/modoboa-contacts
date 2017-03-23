<template>
  <modal :show="true">
    <div slot="header">
      <h3 v-if="pk" class="modal-title">
        <translate>Edit contact</translate></h3>
      <h3 v-else class="modal-title">
        <translate>New contact</translate></h3>
    </div>
    
    <div slot="body">
      <form id="contactForm" class="form-horizontal" method="post" v-on:submit.prevent="saveContact" enctype="multipart/form-data">
        <div class="form-group" :class="{ 'has-error': formErrors['first_name'] || formErrors['last_name'] }">
          <label class="col-sm-1 control-label" for="first_name">
            <span class="fa fa-user"></span></label>
          <div class="col-sm-6">
            <input v-model="contact.first_name" type="text" id="first_name" name="first_name" class="form-control" placeholder="First name">
            <span v-if="formErrors['first_name']" class="help-block">{{ formErrors['first_name'][0] }}</span>
          </div>
          <div class="col-sm-5">
            <input v-model="contact.last_name" type="text" id="last_name" name="last_name" class="form-control" placeholder="Last name">
            <span v-if="formErrors['last_name']" class="help-block">{{ formErrors['last_name'][0] }}</span>
          </div>
        </div>

        <email-field v-for="(email, index) in contact.emails" :index="index" :address="email.address" :type="email.type" :errors="(formErrors.emails) ? formErrors.emails[index] : {}" @updated="(email) => setEmail(index, email)" @add="addEmailField" @delete="(index) => deleteEmailField(index)"></email-field>

        <phone-number-field v-for="(phone_number, index) in contact.phone_numbers" :index="index" :number="phone_number.number" :type="phone_number.type" :errors="(formErrors.phone_numbers) ? formErrors.phone_numbers[index] : {}" @updated="(phone_number) => setPhoneNumber(index, phone_number)" @add="addPhoneNumberField" @delete="(index) => deletePhoneNumberField(index)"></phone-number-field>
        <hr>

        <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
        <input type="submit" class="btn btn-primary" value="Save">

      </form>
    </div>
  </modal>
</template>

<script>
 import { mapActions } from 'vuex'
 import * as api from '../api'
 import EmailField from './EmailField.vue'
 import Modal from './Modal.vue'
 import PhoneNumberField from './PhoneNumberField.vue'
 
 export default {
     components: {
         'email-field': EmailField,
         'modal': Modal,
         'phone-number-field': PhoneNumberField
     },
     data() {
         return {
             contact: {
                 emails: [{}],
                 phone_numbers: [{}]
             },
             formErrors: {},
             show: true
         }
     },
     props: {
         pk: {
             type: Number,
             default: null
         }
     },
     created() {
         if (this.pk) {
             api.getContact(this.pk).then((res) => {
                 this.contact = res.data
                 if (this.contact.phone_numbers.length === 0) {
                     this.contact.phone_numbers.push({})
                 }
             })
         }
     },
     methods: {
         close() {
             this.show = false
             this.contact = {}
             this.formErrors = {}
             this.$emit('close')
         },
         onFormError(response) {
             this.formErrors = response.data
             // FIXME: find a better way to do this
             if (!this.contact.phone_numbers.length) {
                 this.contact.phone_numbers.push({})
             }
         },
         createContact() {
             this.$store.dispatch('createContact', this.contact).then((res) => {
                 this.close()
             }, this.onFormError)
         },
         saveContact() {
             /*var form = document.querySelector('#contactForm')
             var data = new FormData(form)*/

             // FIXME: find a better way to do this
             if (!Object.keys(this.contact.phone_numbers[0]).length) {
                 this.contact.phone_numbers.splice(0, 1)
             }
             if (this.pk !== null) {
                 this.updateContact()
             } else {
                 this.createContact()
             }
         },
         addEmailField() {
             this.contact.emails.push({})
         },
         deleteEmailField(index) {
             this.contact.emails.splice(index, 1)
         },
         setEmail(index, email) {
             this.contact.emails.splice(index, 1, email)
         },
         addPhoneNumberField() {
             this.contact.phone_numbers.push({})
         },
         deletePhoneNumberField(index) {
             this.contact.phone_numbers.splice(index, 1)
         },
         setPhoneNumber(index, phoneNumber) {
             this.contact.phone_numbers.splice(index, 1, phoneNumber)
         },
         updateContact() {
             var args = [this.contact.pk, this.contact]
             this.$store.dispatch('updateContact', args).then((res) => {
                 this.close()
             }, this.onFormError)
         }
     }
 }
</script>
