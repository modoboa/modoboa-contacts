<template>
  <div>
    <h2>
      <span v-if="contact.display_name">{{ contact.display_name }}</span><span v-else>{{ contact.first_name }} {{ contact.last_name }}</span>
      <button type="button" @click="showContactCategoriesForm = true" class="btn btn-default btn-xs"><span class="fa fa-tag"></span></button>
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
            <div class="panel-title"><translate>Summary</translate></div>
          </div>
          <table class="table">
            <tbody>
              <tr v-if="contact.company">
                <td><span class="fa fa-building"></span></td>
                <td colspan="2"><span v-if="contact.position">{{ contact.position }} <translate>at</translate></span> {{ contact.company }}</td>
              </tr>
              <tr v-if="contact.birth_date">
                <td><span class="fa fa-calendar"></span></td>
                <td colspan="2">{{ contact.birth_date|formatDate }}</td>
              </tr>
              <tr v-if="contact.categories">
                <td><span class="fa fa-tag"></span></td>
                <td colspan="2"><span v-for="category in contact.categories" :key="`category-${category}`" class="label label-success">{{ getCategory(category).name }}</span></td>
              </tr>
              <tr v-for="(email, index) in contact.emails" :key="`email-${index}`">
                <td><span v-if="index === 0" class="fa fa-envelope"></span></td>
                <td><a :href="'mailto:' + email.address">{{ email.address }}</a></td>
                <td><span class="label label-info">{{ email.type }}</span></td>
              </tr>
              <tr v-for="(phone, index) in contact.phone_numbers" :key="`phone-${index}`">
                <td><span v-if="index === 0" class="fa fa-phone"></span></td>
                <td>{{ phone.number }}</td>
                <td><span class="label label-info">{{ phone.type }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="contact.address" class="col-sm-6">
        <div class="panel panel-default">
          <div class="panel-heading">
            <div class="panel-title"><span class="fa fa-map-marker"></span> <translate>Address</translate></div>
          </div>
          <div class="panel-body">
            <address>
              {{ contact.address }}<br>
              {{ contact.city }} {{ contact.zipcode }}
              {{ contact.country }} {{ contact.state }}
            </address>
          </div>
        </div>
      </div>
      <div v-if="contact.note" class="col-sm-6">
        <div class="panel panel-default">
          <div class="panel-heading">
            <div class="panel-title"><span class="fa fa-sticky-note"></span> <translate>Note</translate></div>
          </div>
          <div class="panel-body">
            <p>{{ contact.note }}</p>
          </div>
        </div>
      </div>
    </div>

    <contact-categories-form :index="getContactIndex(contact.pk)" v-if="showContactCategoriesForm" @close="showContactCategoriesForm = false"></contact-categories-form>
    <contact-form :pk="contact.pk" v-if="showContactForm" @close="closeContactForm"></contact-form>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ContactCategoriesForm from './ContactCategoriesForm.vue'
import ContactForm from './ContactForm.vue'

export default {
    components: {
        'contact-categories-form': ContactCategoriesForm,
        'contact-form': ContactForm
    },
    data () {
        return {
            showContactCategoriesForm: false,
            showContactForm: false
        }
    },
    computed: mapGetters([
        'contact',
        'categories'
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
        },
        getContactIndex (pk) {
            var result = null
            this.$store.state.list.contacts.forEach((contact, index) => {
                if (contact.pk === pk) {
                    result = index
                }
            })
            return result
        },
        getCategory (pk) {
            for (const category of this.categories) {
                if (category.pk === pk) {
                    return category
                }
            }
            return null
        }
    }
}
</script>
