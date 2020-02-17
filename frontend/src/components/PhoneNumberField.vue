<template>
<div class="form-group" :class="{ 'has-error': errors.number || errors.type }">
    <label for="number" class="col-sm-1 control-label"><span class="fa fa-phone"></span></label>
    <div class="col-sm-6">
        <input v-model="phone.number" type="text" id="number" name="number" class="form-control" :placeholder="phoneNumberPlaceholder">
        <span v-if="errors.number" class="help-block">{{ errors.number[0] }}</span>
    </div>
    <div class="col-sm-3">
        <select v-model="phone.type" id="type" name="type" class="form-control">
            <option v-for="type in types" :value="type" :key="type">{{ type }}</option>
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
        errors: Object,
        index: {
            type: Number,
            required: true
        },
        phone: Object
    },
    data: function () {
        return {
            types: ['cellular', 'fax', 'home', 'main', 'pager', 'work', 'other']
        }
    },
    computed: {
        phoneNumberPlaceholder () {
            return this.$gettext('Phone number')
        }
    }
}
</script>
