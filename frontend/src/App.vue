<template>
  <div id="app">
    <div id="leftcol" class="sidebar collapse navbar-collapse">
      <ul class="nav nav-sidebar" role="menu">
        <router-link tag="li" :to="{ name: 'contact-list' }" exact>
          <a><span class="fa fa-address-book"></span> <translate>Contacts</translate></a>
        </router-link>
        <li class="nav-header"><translate>Categories</translate></li>
        <router-link v-for="category in categories" :key="category.pk" tag="li" :to="{ name: 'contact-list-filtered', params: { category: category.name } }">
          <a><span class="fa fa-tag"></span> {{ category.name }}</a>
        </router-link>
        <li>
          <a href="#" v-on:click.prevent="showCategoryForm = true">
            <span class="fa fa-plus"></span> <translate>Add category</translate>
          </a>
        </li>
      </ul>
    </div>
    <div class="main">
      <router-view></router-view>
    </div>
    <category-form v-if="showCategoryForm" @close="closeCategoryForm"></category-form>
  </div>
</template>

<script>
 import { mapGetters } from 'vuex'
 import CategoryForm from './components/CategoryForm.vue'

 export default {
     components: {
         'category-form': CategoryForm
     },
     computed: mapGetters([
         'categories'
     ]),
     created () {
         this.$store.dispatch('getCategories')
         this.$language.current = 'fr_FR'
     },
     data () {
         return {
             showCategoryForm: false
         }
     },
     methods: {
         closeCategoryForm () {
             this.showCategoryForm = false
         }
     }
 }
</script>
