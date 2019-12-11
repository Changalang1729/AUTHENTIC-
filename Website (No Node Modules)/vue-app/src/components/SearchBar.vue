<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="dark">
            <b-navbar-brand>PoliCheck</b-navbar-brand>
            <b-button class="mr-sm-2" @click="about()" variant="info">About</b-button>
            <b-navbar-nav class="ml-auto">
                <b-nav-form>
                    <b-form-input size="mr-sm-2" v-model="url" class="mr-sm-2" placeholder="Input Article URL"></b-form-input>
                    <b-button class="mr-sm-2" @click="search()">Search</b-button>
                    <b-button class="mr-sm-2" @click="pastResults()">Past Results</b-button>
                </b-nav-form>
            </b-navbar-nav>
        </b-navbar>
    </div>
</template>

<script>
export default {
    data () {
        return{
            // the url being searched
            url: ""
        }
    },
    // emit things on click to tell the display what to show
    methods: {
        search(){
            this.$emit("url", this.url);
        },
        pastResults(){
            this.$emit("pastResults");
        },
        about(){
            this.$emit("about");
        }
    }
}
</script>