<template>
  <div>
    <h2>
      {{ contact.first_name }} {{ contact.last_name }}
      <button type="button" class="btn btn-primary btn-xs" @click="showContactForm = true">
        <span class="fa fa-edit"></span></button>
      <button type="button" class="btn btn-danger btn-xs" @click="deleteContact(contact.pk)">
        <span class="fa fa-trash"></span></button>
    </h2>
    <hr>

    <div class="row">
      <div class="col-sm-6">
        <div class="panel panel-default">
          <div class="panel-heading">
            <div class="panel-title"><translate>Email addresses</translate></div>
          </div>
          <table class="table">
            <tbody>
              <tr v-for="email in contact.emails">
                <td><span class="fa fa-envelope"></span> {{ email.address }}</td>
                <td><span class="label label-info">{{ email.type }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="col-sm-6">
        <div class="panel panel-default">
          <div class="panel-heading">
            <div class="panel-title"><translate>Phone numbers</translate></div>
          </div>
          <table class="table">
            <tbody>
              <tr v-for="phone in contact.phone_numbers">
                <td><span class="fa fa-phone"></span> {{ phone.number }}</td>
                <td><span class="label label-info">{{ phone.type }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    
    <contact-form :pk="contact.pk" v-if="showContactForm" @close="closeContactForm"></contact-form>

  </div>
</template>

<script>
 import { mapGetters } from 'vuex'
 import ContactForm from './ContactForm.vue'

 export default {
     components: {
         'contact-form': ContactForm
     },
     data () {
         return {
             showContactForm: false
         }
     },
     computed: mapGetters([
         'contact'
     ]),
     created () {
         this.$store.dispatch('getContact', this.$route.params.pk)
     },
     methods: {
         closeContactForm () {
             this.showContactForm = false
         },
         deleteContact (pk) {
             this.$store.dispatch('deleteContact', pk).then((res) => {
                 this.$router.push('/')
             })
         }
     }
 }
</script>
