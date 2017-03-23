<template>
  <form class="form-horizontal" role="form">
    <div class="form-group has-feedback">
      <div class="col-sm-12">
        <input class="form-control" type="text"
               :placeholder="$gettext('Search')"
               id="searchquery" name="searchquery" />
        <span class="fa fa-search form-control-feedback"></span>
      </div>
    </div>
  </form>
</template>

<script>
 export default {

 }
</script>
