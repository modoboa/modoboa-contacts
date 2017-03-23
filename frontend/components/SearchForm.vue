<template>
  <form class="form-horizontal" role="form" v-on:submit.prevent="search">
    <div class="form-group has-feedback">
      <div class="col-sm-12">
        <input class="form-control" type="text"
               :placeholder="$gettext('Search')"
               id="searchquery" name="searchquery" v-model="query" />
        <span class="fa fa-search form-control-feedback"></span>
      </div>
    </div>
  </form>
</template>

<script>
 export default {
     data() {
         return {
             query: ''
         }
     },
     methods: {
         search() {
             this.$emit('search', this.query)
         }
     }
 }
</script>
