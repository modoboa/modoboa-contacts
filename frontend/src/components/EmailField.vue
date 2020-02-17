<template>
<div class="form-group" :class="{ 'has-error': errors.address || errors.type }">
    <label for="address" class="col-sm-1 control-label"><span class="fa fa-envelope"></span></label>
    <div class="col-sm-6">
        <input v-model="email.address" type="email" id="address" name="address" class="form-control" :placeholder="addressPlaceholder">
        <span v-if="errors.address" class="help-block">{{ errors.address[0] }}</span>
    </div>
    <div class="col-sm-3">
        <select v-model="email.type" id="type" name="type" class="form-control">
            <option v-for="type in types" :value="type"
                    :key="type">{{ type }}
            </option>
        </select>
        <span v-if="errors.type" class="help-block">{{ errors.type[0] }}</span>
    </div>
    <div class="col-sm-2">
        <a href="#" v-on:click.prevent="$emit('add')"><span class="fa fa-plus"></span></a>
        <a v-if="index" href="#" v-on:click.prevent="$emit('delete', index)"><span class="fa fa-trash"></span></a>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        email: Object,
        errors: Object,
        index: {
            type: Number,
            required: true
        }
    },
    data: function () {
        return {
            types: ['home', 'work', 'other']
        }
    },
    computed: {
        addressPlaceholder () {
            return this.$gettext('Address')
        }
    }
}
</script>
