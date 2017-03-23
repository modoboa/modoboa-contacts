<template>
  <div class="modal-mask" v-show="show" transition="modal">
    <div class="modal" style="display: block">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <slot name="header"></slot>
          </div>
          <div class="modal-body">
            <slot name="body"></slot>
          </div>
          <div v-if="showFooter" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
 export default {
     props: {
         show: {
             type: Boolean,
             required: true,
             twoWay: true
         },
         showFooter: {
             type: Boolean,
             default: false
         }
     }
 }
</script>

<style>
 .modal-mask {
     position: fixed;
     z-index: 9998;
     top: 0;
     left: 0;
     width: 100%;
     height: 100%;
     background-color: rgba(0, 0, 0, .5);
     display: table;
     transition: opacity .3s ease;
 }
</style>
