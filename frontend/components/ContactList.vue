<template>
  <div>
    <div class="row">
      <div class="col-sm-5">
        <search-form @search="(query) => getContacts(query)"></search-form>
      </div>
      <div class="col-sm-7">
        <button type="button" class="btn btn-primary" @click="showContactForm = true">
          <span class="fa fa-plus"></span> <translate>Add</translate>
        </button>
      </div>
    </div>
    <table v-if="contacts" class="table">
      <thead>
        <tr>
          <th><translate>Display name</translate></th>
          <th><translate>Email</translate></th>
          <th><translate>Phone</translate></th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contact in contacts">
          <td>{{ contact.first_name }} {{ contact.last_name }}</td>
          <td>{{ contact.emails[0].address }}</td>
          <td v-if="contact.phone_numbers.length">{{ contact.phone_numbers[0].number }}</td>
          <td v-else></td>
          <td class="text-right">
            <button type="button" @click="editContact(contact.pk)" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-edit"></span></button>
            <button type="button" @click="deleteContact(contact.pk)" class="btn btn-danger btn-xs"><span class="glyphicon glyphicon-trash"></span></button>
          </td>
        </tr>
      </tbody>
    </table>
    <contact-form :pk="currentContactPk" v-if="showContactForm" @close="closeContactForm"></contact-form>
  </div>
</template>

<script>
 import { mapActions, mapState } from 'vuex'
 import ContactForm from './ContactForm.vue'
 import SearchForm from './SearchForm.vue'
 
 export default {
     components: {
         'contact-form': ContactForm,
         'search-form': SearchForm
     },
     data() {
         return {
             currentContactPk: null,
             showContactForm: false
         }
     },
     props: {
         pk: null
     },
     computed: mapState([
         'contacts'
     ]),
     created() {
         this.getContacts()
     },
     methods: {
         getContacts(query) {
             this.$store.dispatch('getContacts', query)
         },
         closeContactForm() {
             this.showContactForm = false
             this.currentContactPk = null
         },
         deleteContact(pk) {
             this.$store.dispatch('deleteContact', pk)
         },
         editContact(pk) {
             this.currentContactPk = pk
             this.showContactForm = true
         }
     }
 }
</script>
