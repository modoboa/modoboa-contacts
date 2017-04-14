<template>
  <modal :show="true">
    <div slot="header">
      <h3 class="modal-title"><translate>Add category</translate></h3>
    </div>
    <div slot="body">
      <form id="categoryForm" class="form-horizontal" method="post" v-on:submit.prevent="createCategory">
        <div class="form-group" :class="{ 'has-error': formErrors['name'] }">
          <div class="col-sm-7">
            <input v-model="category.name" type="text" id="name" name="name" class="form-control" :placeholder="namePlaceholder">
            <span v-if="formErrors['name']" class="help-block">{{ formErrors['name'][0] }}</span>
          </div>
        </div>
        <hr>
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
 import Modal from './Modal.vue'

 export default {
     components: {
         'modal': Modal
     },
     data () {
         return {
             category: {},
             formErrors: {}
         }
     },
     computed: {
         namePlaceholder () {
             return this.$gettext('Name')
         }
     },
     methods: {
         close () {
             this.show = false
             this.category = {}
             this.formErrors = {}
             this.$emit('close')
         },
         createCategory () {
             this.$store.dispatch('createCategory', this.category).then((res) => {
                 this.close()
             }, this.onFormError)
         },
         onFormError (response) {
             this.formErrors = response.data
         }
     }
 }
</script>
