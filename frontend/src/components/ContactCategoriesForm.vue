<template>
  <modal :show="true">
    <div slot="header">
      <h3 class="modal-title"><translate>Categories</translate></h3>
    </div>

    <div slot="body">
      <form id="categoriesForm" class="form-horizontal" method="post" v-on:submit.prevent="saveCategories()">
        <div v-for="category in categories" :key="category.pk" class="form-group">
          <div class="col-sm-offset-1 col-sm-11">
            <div class="checkbox">
              <label>
                <input type="checkbox" :value="category.pk" v-model="checkedCategories"> {{ category.name }}
              </label>
            </div>
          </div>
        </div>
        <hr>
        <div class="pull-right">
          <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
          <input type="submit" class="btn btn-primary" :value="'Apply' | translate">
        </div>
        <div class="clearfix"></div>
      </form>
    </div>
  </modal>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    computed: mapGetters([
        'categories'
    ]),
    data () {
        return {
            checkedCategories: []
        }
    },
    props: {
        index: {
            type: Number,
            required: true
        }
    },
    methods: {
        close () {
            this.$emit('close')
        },
        saveCategories () {
            var contact = JSON.parse(
                JSON.stringify(this.$store.state.list.contacts[this.index]))
            contact.categories = this.checkedCategories
            this.$store.dispatch('updateContact', [contact.pk, contact]).then(res => {
                this.close()
            })
        }
    },
    created () {
        this.checkedCategories = this.$store.state.list.contacts[this.index].categories
    }
}
</script>
