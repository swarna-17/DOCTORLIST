<template>
    <div>
        <h2>
            DOCTORLIST
        </h2>
        <input type="text" v-model="keyword" @input="getresults" placeholder="Search Doctors Data"/>
        <p>Results are :</p>
        <div>
            <center>
            <table border="5px solid black" width="50%" border-spacing:1px >
                
                <tr>
                <td style="text-align:center"><em><strong>NAME</strong></em></td>
                <td style="text-align:center"><em><strong>JOB</strong></em></td>
                <td style="text-align:center"><em><strong>COUNTRY</strong></em></td>
                </tr>
                <tr v-for="item in list" v-bind:key="item.name">
                <td>{{item.name}}</td>
                <td>{{item.job}}</td>
                <td>{{item.country}}</td>
                </tr>
            </table>
            </center>
        </div>    
    </div>
</template>
<script>
//import Vue from 'vue';
//import VueAxios from 'vue-axios';
import axios from 'axios';
//Vue.use(VueAxios,axios)
export default{
        name:"Users",
        data(){
            return{
                keyword:'',
                list : [],
            }
        },
        watch:{
            keyword:function(val){
                if(val.length > 3){
                    this.getresults();
                }
            }
        },
        methods:
        {
            getresults(){
                axios.get('http://127.0.0.1:8000/doctors/?search='+this.keyword)
                .then(resp=>{
                    this.list=resp.data
                    console.log(resp)
                })}
        },
        created(){
            this.getresults()
        }
    }
</script>
