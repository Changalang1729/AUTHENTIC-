<template>
    <div class="fixed">
        <SearchBar @url="showData" @pastResults="showPastResults" @about="about" />
        <div class="container-fluid" v-show="dataReady">
            <div class="row">
                <div class="col-4">
                    <div>
                        <br><br><br><br>
                        <apexchart width="450" type="donut" :options="chartOptions" :series="series"></apexchart>
                    </div>
                </div>
                <div class="col-8">
                    <b-card class="text-center" header-tag="header" footer-tag="footer">
                        <template v-slot:header >
                            <h2 class="mb-0">{{ title }}</h2>
                        </template>
                        
                        <b-list-group class="text-left">
                            <b-list-group-item><b>Author: </b>{{ authors }} 
                            <span class="float-right"><b-button variant="secondary" @click="goToSite">View Site</b-button></span>
                            </b-list-group-item>
                            <b-list-group-item><b>Organization: </b>{{ company }}</b-list-group-item>
                        </b-list-group>
                        <br>
                        <b-list-group class="text-left">
                            <b-list-group-item>
                                <div id="scrollspy-nested" style="position:relative; height:350px; overflow-y:auto">
                                    <p> {{ text }}</p>
                                </div>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </div>
            </div>
        </div>

        <div v-show="showTable">
            <table class="table ">
                <thead>
                    <tr>
                        <th>  
                            <b-input-group class="ml-3-auto">
                                <b-form-input class="text-right" v-model="query" placeholder="Input Company or Article Title and Click Selected Search Type"></b-form-input>
                                <b-input-group-append>
                                <div class="btn-group">
                                    <b-button variant="secondary" @click="showCompany">Company</b-button>
                                    <b-button variant="dark" @click="showArticle">Article Title</b-button>
                                </div>
                                </b-input-group-append>
                            </b-input-group>
                        </th>
                    </tr>
                </thead>
            </table>
            <b-table :items="items" :fields="fields" striped responsive="sm">
                <template v-slot:cell(show_more)="row">
                    <b-button size="sm" @click="showData(row.item.url)" class="mr-2">
                        Details
                    </b-button>
                </template>       
            </b-table>
        </div>

        <div v-show="showAbout">
            <About />
        </div>

    </div>
</template>

<script>
import Vue from 'vue'
import VueApexCharts from 'vue-apexcharts'
import SearchBar from './SearchBar.vue'
import About from './About.vue'

Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

export default {
    data: function() {
        return {
            // for the chart
            series: [],
            fill: {
                type: "solid",
            },
            chartOptions: {
                chart:{
                    background: "transparent",
                },
                legend: {
                    show: false
                },
                labels: ["Conservative", "Liberal"],
                colors: ['#FF0000', '#0000FF'],        
            },
            // display things
            text: "",
            title: "TITLE",
            authors: "",
            company: "",
            link: "",
            dataReady: false,
            showTable: false,
            showAbout: true,
            articleCheckUrl: "http://127.0.0.1:5000/article?article=",
            results: "",
            // past results and table stuff
            storedResults: [],
            organizations: [],
            fields: ["Organization", "Title", "Conservative", "Liberal", {key: 'show_more', thStyle: {display: 'none'}}],
            items: [],
            query: ""
        }
    },
    components: {
        SearchBar,
        About
    },
    // fetch past results
    mounted: async function(){
        this.fetchPastResults()
    },
    methods: {
        // fetches past results
        async fetchPastResults(){
            let response = await fetch("http://127.0.0.1:5000/results");
            this.results = await response.json();
            this.addOrganizations();
        },
        // stores all of the results by organization in an easier to use format than the json I returned
        async addOrganizations(){
            let values = Object.values(this.results);
            let objects = Object.values(values);
            objects.forEach(object => {

                let conservative = parseInt(object.article.bias.conservative * 100);
                let liberal = parseInt(object.article.bias.liberal * 100);

                if (conservative < 0){
                    conservative = Math.abs(conservative);
                    if (conservative < liberal){
                        liberal = conservative;
                        conservative = 100 - liberal;
                    }
                    else{
                        liberal = 100 - conservative;
                    }
                }

                else{
                    liberal = Math.abs(liberal);
                    if (liberal < conservative){
                        conservative = liberal;
                        liberal = 100 - conservative;
                    }
                    else{
                        conservative = 100 - liberal;
                    }
                }

                if (object.article.company == "ashingtonpost"){
                        object.article.company = "washingtonpost"
                }
                this.storedResults.push({"company": object.article.company, "conservative": conservative, "liberal": liberal, "title": object.article.title, "url": object.article.url})
            });
            objects.forEach(object => {
                if (!this.organizations.includes(object.article.company)){
                    this.organizations.push(object.article.company)
                }
            });
        },
        // fetches info from a url query
        async fetchInfo(url){
            let response = await fetch("http://127.0.0.1:5000/article?article=" + url);
            response = await fetch("http://127.0.0.1:5000/article?article=" + url);
            let responseJson = await response.json();
            return responseJson;
        },
        // shows the data
        async showData(url){
            let responseJson = await this.fetchInfo(url);
            this.title = await responseJson.article.title;

            // format authors
            this.authors = await responseJson.article.authors;
            this.authors = this.authors.replace("'", "");
            this.authors = this.authors.replace("'", "");
            this.authors = this.authors.replace("[", "");
            this.authors = this.authors.replace("]", "");

            this.company = responseJson.article.company.toUpperCase();
            if (this.company == "ASHINGTONPOST"){
                this.company = "WASHINGTONPOST"
            }

            this.text = responseJson.article.text;

            this.link = responseJson.article.url

            let conservative = parseInt(responseJson.article.bias.conservative * 100);
            let liberal = parseInt(responseJson.article.bias.liberal * 100);

                if (conservative < 0){
                    conservative = Math.abs(conservative);
                    if (conservative < liberal){
                        liberal = conservative;
                        conservative = 100 - liberal;
                    }
                    else{
                        liberal = 100 - conservative;
                    }
                }

                else{
                    liberal = Math.abs(liberal);
                    if (liberal < conservative){
                        conservative = liberal;
                        liberal = 100 - conservative;
                    }
                    else{
                        conservative = 100 - liberal;
                    }
                }

            if (conservative < liberal){
                conservative = Math.abs(conservative);
                liberal = 100 - conservative;
            }
            else{
                liberal = Math.abs(liberal);
                conservative = 100 - liberal;
            }

            this.series = [conservative, liberal];
            if (url){
                this.showTable = false;
                this.showAbout = false
                this.dataReady = true;
            }
            this.articleCheckUrl = url;

            this.dataReady = true;
        },

        // show the past results
        showPastResults(){
            this.items = [];
            this.storedResults.forEach(result => {
                this.items.push({'Organization': result.company.toUpperCase(), 'FullTitle': result.title, 'Title': this.trimTitle(result.title), 'Conservative': result.conservative, 'Liberal': result.liberal, 'url': result.url});
            });
            this.items.sort();
            this.dataReady = false;
            this.showAbout = false;
            this.showTable = true;
        },

        // trims the title for the table
        trimTitle (title){
            if (title.length <= 50){
                return title;
            }
            else{
                return (title.slice(0, 50) + " ...");
            }
        },

        // shows the about page
        about(){
            this.dataReady = false;
            this.showTable = false;
            this.showAbout = true;
        },

        // does a search for the company the user queried
        showCompany(){
            this.items = [];
            this.storedResults.forEach(result => {
                if (result.company.toLowerCase().replace(/\s/g, '').includes(this.query.toLowerCase().replace(/\s/g, ''))){
                    this.items.push({'Organization': result.company.toUpperCase(), 'FullTitle': result.title, 'Title': this.trimTitle(result.title), 'Conservative': result.conservative, 'Liberal': result.liberal, 'url': result.url});
                }
            });
            this.items.sort()
        },

        // does a search for the article(s) the user queried
        showArticle(){
            this.items = [];
            this.storedResults.forEach(result => {
                if (result.title.toLowerCase().replace(/\s/g, '').includes(this.query.toLowerCase().replace(/\s/g, ''))){
                    this.items.push({'Organization': result.company.toUpperCase(), 'FullTitle': result.title, 'Title': this.trimTitle(result.title), 'Conservative': result.conservative, 'Liberal': result.liberal, 'url': result.url});
                }
            });
            this.items.sort()            
        },
        // open a linked website in a new tab
        goToSite(){
            window.open(this.link, '_blank');
        }
    }
};
</script>

<style scoped>
.table {
    margin-bottom: 0
    }
.b-tabel{
    margin-top: 0
    }
</style>