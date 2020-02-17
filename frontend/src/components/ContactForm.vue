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
            <input v-model="contact.first_name" type="text" id="first_name" name="first_name" class="form-control" :placeholder="firstNamePlaceholder">
            <span v-if="formErrors['first_name']" class="help-block">{{ formErrors['first_name'][0] }}</span>
          </div>
          <div class="col-sm-5">
            <input v-model="contact.last_name" type="text" id="last_name" name="last_name" class="form-control" :placeholder="lastNamePlaceholder">
            <span v-if="formErrors['last_name']" class="help-block">{{ formErrors['last_name'][0] }}</span>
          </div>
        </div>
        <div class="form-group" :class="{ 'has-error': formErrors['display_name'] }">
          <div class="col-sm-offset-1 col-sm-11">
            <input v-model="contact.display_name" type="text" id="display_name" name="display_name" class="form-control" :placeholder="displayNamePlaceholder">
            <span v-if="formErrors['display_name']" class="help-block">{{ formErrors['display_name'][0] }}</span>
          </div>
        </div>
        <div class="form-group" :class="{ 'has-error': formErrors['company'] || formErrors['position'] }">
          <label class="col-sm-1 control-label" for="company">
            <span class="fa fa-building"></span></label>
          <div class="col-sm-6">
            <input v-model="contact.company" type="text" id="company" name="company" class="form-control" :placeholder="companyPlaceholder">
            <span v-if="formErrors['company']" class="help-block">{{ formErrors['company'][0] }}</span>
          </div>
          <div class="col-sm-5">
            <input v-model="contact.position" type="text" id="position" name="position" class="form-control" :placeholder="positionPlaceholder">
            <span v-if="formErrors['position']" class="help-block">{{ formErrors['position'][0] }}</span>
          </div>
        </div>

        <email-field v-for="(email, index) in contact.emails"
                     :key="`email-${index}`"
                     :index="index"
                     :email="email"
                     :errors="(formErrors.emails) ? formErrors.emails[index] : {}"
                     @add="addEmailField"
                     @delete="(index) => deleteEmailField(index)">
        </email-field>

        <phone-number-field v-for="(phone_number, index) in contact.phone_numbers"
                            :key="`phone-${index}`"
                            :index="index"
                            :phone="phone_number"
                            :errors="(formErrors.phone_numbers) ? formErrors.phone_numbers[index] : {}"
                            @add="addPhoneNumberField"
                            @delete="(index) => deletePhoneNumberField(index)">
        </phone-number-field>

        <div v-if="showMore">
          <div class="form-group" :class="{ 'has-error': formErrors['birth_date'] }">
            <label class="col-sm-1 control-label" for="birth_date">
              <span class="fa fa-calendar"></span></label>
            <div class="col-sm-6">
              <datepicker v-model="contact.birth_date" id="birth_date" name="birth_date" inputClass="form-control" :placeholder="birthDatePlaceholder"></datepicker>
              <span v-if="formErrors['birth_date']" class="help-block">{{ formErrors['birth_date'][0] }}</span>
            </div>
          </div>
          <div class="form-group" :class="{ 'has-error': formErrors['address'] }">
            <label class="col-sm-1 control-label" for="address">
              <span class="fa fa-map-marker"></span></label>
            <div class="col-sm-11">
              <input v-model="contact.address" type="text" id="address" name="address" class="form-control" :placeholder="addressPlaceholder">
              <span v-if="formErrors['address']" class="help-block">{{ formErrors['address'][0] }}</span>
            </div>
          </div>
          <div class="form-group" :class="{ 'has-error': formErrors['zipcode'] || formErrors['city'] }">
            <div class="col-sm-offset-1 col-sm-4">
              <input v-model="contact.zipcode" type="text" id="zipcode" name="zipcode" class="form-control" :placeholder="zipCodePlaceholder">
              <span v-if="formErrors['zipcode']" class="help-block">{{ formErrors['zipcode'][0] }}</span>
            </div>
            <div class="col-sm-7">
              <input v-model="contact.city" type="text" id="city" name="city" class="form-control" :placeholder="cityPlaceholder">
              <span v-if="formErrors['city']" class="help-block">{{ formErrors['city'][0] }}</span>
            </div>
          </div>
          <div class="form-group" :class="{ 'has-error': formErrors['country'] || formErrors['state'] }">
            <div class="col-sm-offset-1 col-sm-6">
              <input v-model="contact.country" type="text" id="country" name="country" class="form-control" :placeholder="countryPlaceholder">
              <span v-if="formErrors['country']" class="help-block">{{ formErrors['country'][0] }}</span>
            </div>
            <div class="col-sm-5">
              <input v-model="contact.state" type="text" id="state" name="state" class="form-control" :placeholder="statePlaceholder">
              <span v-if="formErrors['state']" class="help-block">{{ formErrors['state'][0] }}</span>
            </div>
          </div>
          <div class="form-group">
            <label class="col-sm-1 control-label" for="address">
              <span class="fa fa-sticky-note"></span></label>
            <div class="col-sm-11">
              <textarea v-model="contact.note" id="note" name="note" class="form-control" :placeholder="notePlaceholder"></textarea>
            </div>
          </div>
        </div>

        <hr>
        <button type="button" class="btn btn-default" @click="showMore = true"><translate>More</translate></button>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <input type="submit" class="btn btn-primary" value="Save">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
import * as api from '../api'
import Datepicker from 'vuejs-datepicker'
import EmailField from './EmailField.vue'
import Modal from './Modal.vue'
import PhoneNumberField from './PhoneNumberField.vue'

export default {
    components: {
        datepicker: Datepicker,
        'email-field': EmailField,
        modal: Modal,
        'phone-number-field': PhoneNumberField
    },
    data () {
        return {
            contact: {
                emails: [{}],
                phone_numbers: [{}]
            },
            formErrors: {},
            show: true,
            showMore: false
        }
    },
    computed: {
        firstNamePlaceholder () {
            return this.$gettext('First name')
        },
        lastNamePlaceholder () {
            return this.$gettext('Last name')
        },
        displayNamePlaceholder () {
            return this.$gettext('Display name')
        },
        companyPlaceholder () {
            return this.$gettext('Company')
        },
        positionPlaceholder () {
            return this.$gettext('Position')
        },
        birthDatePlaceholder () {
            return this.$gettext('Birth date')
        },
        addressPlaceholder () {
            return this.$gettext('Address')
        },
        zipCodePlaceholder () {
            return this.$gettext('Zip Code')
        },
        cityPlaceholder () {
            return this.$gettext('City')
        },
        countryPlaceholder () {
            return this.$gettext('Country')
        },
        statePlaceholder () {
            return this.$gettext('State/Province')
        },
        notePlaceholder () {
            return this.$gettext('Note')
        }
    },
    props: {
        pk: {
            type: Number,
            default: null
        }
    },
    created () {
        if (this.pk) {
            api.getContact(this.pk).then((res) => {
                this.contact = res.data
                if (this.contact.emails.length === 0) {
                    this.contact.emails.push({})
                }
                if (this.contact.phone_numbers.length === 0) {
                    this.contact.phone_numbers.push({})
                }
                if (this.contact.address !== '') {
                    this.showMore = true
                }
            })
        }
    },
    methods: {
        close () {
            this.show = false
            this.contact = {}
            this.formErrors = {}
            this.$emit('close')
        },
        onFormError (response) {
            this.formErrors = response.data
        },
        createContact (contact) {
            this.$store.dispatch('createContact', contact).then((res) => {
                this.close()
            }, this.onFormError)
        },
        saveContact () {
            var contact = JSON.parse(JSON.stringify(this.contact))
            /* var form = document.querySelector('#contactForm')
             var data = new FormData(form) */

            if (!Object.keys(contact.phone_numbers[0]).length) {
                contact.phone_numbers.splice(0, 1)
            }
            if (contact.birth_date) {
                contact.birth_date = contact.birth_date.split('T')[0]
            }
            if (this.pk !== null) {
                this.updateContact(contact)
            } else {
                this.createContact(contact)
            }
        },
        addEmailField () {
            this.contact.emails.push({})
        },
        deleteEmailField (index) {
            this.contact.emails.splice(index, 1)
        },
        setEmail (index, email) {
            this.contact.emails.splice(index, 1, email)
        },
        addPhoneNumberField () {
            this.contact.phone_numbers.push({})
        },
        deletePhoneNumberField (index) {
            this.contact.phone_numbers.splice(index, 1)
        },
        setPhoneNumber (index, phoneNumber) {
            this.contact.phone_numbers.splice(index, 1, phoneNumber)
        },
        updateContact (contact) {
            var args = [contact.pk, contact]
            this.$store.dispatch('updateContact', args).then((res) => {
                this.close()
            }, this.onFormError)
        }
    }
}
</script>
