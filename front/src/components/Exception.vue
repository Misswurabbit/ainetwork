<template>
    <div class="warning_container">
        <ul class="nav nav-tabs" >
            <li class="nav-item">
                <a  class="nav-link" @click="back">返回</a>
            </li>
        </ul>
    <BootstrapTable class="warning"
            ref="table"
            :columns="columns"
            :data="data"
            :options="options"
    />
    </div>
</template>

<script>
    import Axios from 'axios'

    function getJson(that, url) {
        Axios.get(url).then(response => {
            that.data = response.data.data;
        }).catch((error) => {
            window.console.log(error);
        });
    }
    export default {
        name: "Exception",
        props:['id'],
        data(){
            return {
                // data:[{
                //     anomoly: [
                //         "net",
                //         "cpu",
                //         "disk"
                //     ],
                //     anomoly_type: "1,2,4",
                //     time_stamp: "2014-01-08 23:51:20"
                // },
                //     {
                //         anomoly: [
                //             "net",
                //             "cpu",
                //             "disk"
                //         ],
                //         anomoly_type: "1,2,4",
                //         time_stamp: "2014-01-08 23:51:20"
                //     }],
                data:[{  anomoly: [
                        "net",
                        "cpu",
                        "disk"
                    ],
                    anomoly_type: "1,2,4",
                    time_stamp: "2014-01-08 23:51:20"
                }],
                columns: [
                    {
                        title: '时间窗口',
                        field: 'time_stamp',
                    }, {
                        field: 'anomoly',
                        title: '描述'
                    }
                ],
                options: {
                    //showColumns: true,
                    pagination: true,
                    pageSize: 10,
                }
            }
        },
        created(){
            getJson(this,"http://[2001:da8:270:2020:f816:3eff:fe20:a164]:8080/warning/"+ this.$props.id)
        },
        methods:{
            back(){
                this.$router.back(-1);
            }
        }

    }
</script>

<style scoped>
.warning_container{
    width: 80%;
    margin-left: 10%;
}
</style>