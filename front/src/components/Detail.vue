<template>
    <div class="tgcontainer">
        <div>
            <ul class="nav nav-tabs" >
                <li class="nav-item">
                    <a :class="menuStyle1" @click="tableClicked">数据总览</a>
                </li>
                <li class="nav-item">
                    <a  :class="menuStyle2" @click="graphClicked">图表展示</a>
                </li>
                <li class="nav-item">
                    <a  class="nav-link" @click="back">返回</a>
                </li>
            </ul>
        </div>
        <div v-if="item==0">
            <BootstrapTable
                    ref="table"
                    :columns="columns"
                    :data="data"
                    :options="options"
            />
        </div>
        <div class="show" v-if="item==1">
        <line-graph v-for="(value, key) in gData" :content='value'></line-graph>

        </div>
    </div>
</template>

<script>
    import Axios from 'axios'
    import LineGraph from './LineGraph'

    function constructor(data){
        let cs = [];
        let type = ['cpu_util_percent','disk_io_percent','mem_util_percent','net_in'];
        for(var i=0;i<type.length;i++){
            let temp = {
                TV:[],
                TVE:[],
                name:type[i]
            }
            for (var j=0;j<data.length;j++){
                temp.TV.push([j,data[j][type[i]]])
                if (data[j]['predict_status']==1)
                    temp.TVE.push([j,data[j][type[i]]])

            }
            cs.push(temp)
        }
        return cs;
    }
    function getJson(that, url) {
        Axios.get(url).then(response => {
            that.data = response.data.data
            that.gData = constructor(response.data.data);
            //window.console.log(that.gData)
        }).catch((error) => {
            window.console.log(error);
        });
    }

    export default {
        name: "Detail",
        props: ["id"],
        components:{
            LineGraph:LineGraph
        },
        created() {
            getJson(this, "http://[2001:da8:270:2020:f816:3eff:fe20:a164]:8080/detail/" + this.$props.id);
            this.intervalId = setInterval(() => {
                getJson(this,"http://[2001:da8:270:2020:f816:3eff:fe20:a164]:8080/detail/" + this.$props.id)
            }, 3600)
        },
        data() {
            return {
                columns: [
                    {
                        title: '机器ID',
                        field: 'machine_id',
                        align: 'center',

                    },
                    {
                        field: 'cpu_util_percent',
                        title: 'CPU利用率',
                        align: 'center',

                    },
                    {
                        field: 'disk_io_percent',
                        title: '磁盘利用率',
                        align: 'center',

                    },
                    {
                        field: 'mem_util_percent',
                        title: '内存利用率',
                        align: 'center',
                    },
                    {
                        field: 'net_in',
                        title: '进网',
                        align: 'center',

                    },
                    {
                        field: 'time_stamp',
                        title: '时间',
                        align: 'center',

                    }
                ],
                data: [],
                gData:[],
                options: {
                    //showColumns: true,
                    pagination: true,
                    pageSize: 10,

                },
                item:0,
                menuStyle1:"nav-link active",
                menuStyle2:"nav-link"
            }
        },
        methods: {
            tableClicked(){
                this.item = 0;
                this.menuStyle1 = "nav-link active";
                this.menuStyle2 = "nav-link";
            },
            graphClicked(){
                this.item = 1;
                this.menuStyle1 = "nav-link";
                this.menuStyle2 = "nav-link active";
            },
            back(){
                this.$router.back(-1);
            }
        }
    }
</script>

<style scoped>
    .tgcontainer {
        width: 80%;
        margin-left: 10%;
        margin-top: 36px;
    }

    #detail {
        width: 80%;
    }
    .show{
        width: 100%;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content:space-around;
    }
</style>