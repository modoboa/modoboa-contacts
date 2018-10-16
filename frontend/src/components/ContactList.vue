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
        <button type="button" class="btn btn-default" @click="showInfo = true">
          <span class="fa fa-info-circle"></span>
        </button>
        <button v-if="abookSynced === false"
                class="btn btn-success"
                @click="launchAbookSync">
          <translate>Synchronize your address book</translate>
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
        <tr v-for="(contact, index) in contacts" :key="contact.pk">
          <td><router-link :to="{ name: 'contact-detail', params: { pk: contact.pk } }"><span v-if="contact.display_name">{{ contact.display_name }}</span><span v-else>{{ contact.first_name }} {{ contact.last_name }}</span></router-link></td>
          <td v-if="contact.emails.length">{{ contact.emails[0].address }}</td>
          <td v-else></td>
          <td v-if="contact.phone_numbers.length">{{ contact.phone_numbers[0].number }}</td>
          <td v-else></td>
          <td class="text-right">
            <button type="button" @click="editContactCategories(index)" class="btn btn-default btn-xs"><span class="fa fa-tag"></span></button>
            <button type="button" @click="editContact(contact.pk)" class="btn btn-primary btn-xs"><span class="fa fa-edit"></span></button>
            <button type="button" @click="deleteContact(contact.pk)" class="btn btn-danger btn-xs"><span class="fa fa-trash"></span></button>
          </td>
        </tr>
      </tbody>
    </table>
    <contact-categories-form :index="contactIndex" v-if="showContactCategoriesForm" @close="closeContactCategoriesForm"></contact-categories-form>
    <contact-form :pk="currentContactPk" v-if="showContactForm" @close="closeContactForm"></contact-form>
    <addressbook-detail v-if="showInfo" @close="showInfo = false" :addressbook="addressBook">
    </addressbook-detail>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import * as api from '@/api'
import AddressBookDetail from './AddressBookDetail.vue'
import ContactCategoriesForm from './ContactCategoriesForm.vue'
import ContactForm from './ContactForm.vue'
import SearchForm from './SearchForm.vue'

export default {
    components: {
        'contact-categories-form': ContactCategoriesForm,
        'contact-form': ContactForm,
        'search-form': SearchForm,
        'addressbook-detail': AddressBookDetail
    },
    data () {
        return {
            currentContactPk: null,
            contactIndex: null,
            showContactForm: false,
            showContactCategoriesForm: false,
            abookSynced: window.userProfile ? window.userProfile.abookSynced : true,
            showInfo: false,
            addressBook: null
        }
    },
    props: {
        pk: null
    },
    computed: {
        ...mapGetters([
            'contacts'
        ])
    },
    created () {
        this.getContacts(this.$route.params)
        api.getDefaultAddressBook().then(response => {
            this.addressBook = response.data
        })
    },
    methods: {
        getContacts (query, category) {
            this.$store.dispatch('getContacts', [query, category])
        },
        closeContactCategoriesForm () {
            this.showContactCategoriesForm = false
            this.contactIndex = null
        },
        closeContactForm () {
            this.showContactForm = false
            this.currentContactPk = null
        },
        deleteContact (pk) {
            this.$store.dispatch('deleteContact', pk)
        },
        editContact (pk) {
            this.currentContactPk = pk
            this.showContactForm = true
        },
        editContactCategories (index) {
            this.contactIndex = index
            this.showContactCategoriesForm = true
        },
        launchAbookSync () {
            api.syncAddressBook().then(response => {
                this.abookSynced = true
                window.location.reload()
            })
        }
    },
    watch: {
        '$route' (to, from) {
            this.getContacts(this.$route.params)
        }
    }
}
</script>
