<template>
<modal :show="true">
    <div slot="header">
        <h3 v-if="category.pk" class="modal-title"><translate>Edit category</translate></h3>
        <h3 v-else class="modal-title"><translate>Add category</translate></h3>
    </div>
    <div slot="body">
        <form id="categoryForm" class="form-horizontal" method="post" v-on:submit.prevent="createCategory">
            <div class="form-group" :class="{ 'has-error': formErrors.name }">
                <div class="col-sm-7">
                    <input v-model="category.name" type="text" id="name" name="name" class="form-control" :placeholder="namePlaceholder">
                    <span v-if="formErrors.name" class="help-block">{{ formErrors.name[0] }}</span>
                </div>
            </div>
            <hr>
            <div class="pull-right">
                <button type="button" class="btn btn-default" @click="close"><translate>Close</translate></button>
                <input type="submit" class="btn btn-primary" :value="'Save' | translate">
            </div>
            <div class="clearfix"></div>
        </form>
    </div>
</modal>
</template>

<script>
export default {
    props: {
        initialCategory: {
            type: Object,
            default: () => { return {} }
        }
    },
    data () {
        return {
            category: JSON.parse(JSON.stringify(this.initialCategory)),
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
            var action = (this.category.pk) ? 'updateCategory' : 'createCategory'
            var category = JSON.parse(JSON.stringify(this.category))
            this.$store.dispatch(action, category).then((res) => {
                this.close()
            }, this.onFormError)
        },
        onFormError (response) {
            this.formErrors = response.data
        }
    }
}
</script>
