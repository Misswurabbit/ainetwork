<template>
    <div>
    <div class="container">
        <div id="myCharts" ref="myCharts" :style="{height: '300px', width:'600px'}"></div>
        <BootstrapTable
                        ref="tableE"
                        :columns="columnsE"
                        :data="data.warning_data"
                        :options="optionsE"
                        @onPostBody="vueFormatterPostBody"
        />


        <div class="foot">
        <BootstrapTable
                        ref="table"
                        :columns="columns"
                        :data="data.data"
                        :options="options"
                        @onPostBody="vueFormatterPostBody"
        />
        </div>
    </div>
    </div>
</template>

<script>
    import tableMixin from '../mixins/table'
    import Axios from 'axios'

    function constructor(orign) {
        var dic = {
            warning_type: ['total'],
            warning_count: [],
            data: {},
            warning_data: {}
        };

        for (var key in orign) {
            if (!Array.isArray(orign[key])) {
                dic.warning_type.push(key.substring(0, key.length - 8));
                dic.warning_count.push(orign[key])
            }
            else {
                if (key == 'data') {
                    dic.data = orign[key]
                    dic.warning_count.unshift(orign[key].length)
                }
                else
                    dic.warning_data = orign[key]
            }
        }
        return dic
    }

    function getJson(that, url) {
        Axios.get(url).then(response => {
            that.data = constructor(response.data);
            initBar(that)
        }).catch((error) => {
            window.console.log(error);
        });
    }

    function initBar(that) {
        const myCharts = that.$echarts.init(that.$refs.myCharts);
        let options = {
            title: {
                text: "总览",   //图表顶部的标题
            },
            tooltip: {   //鼠标悬浮框的提示文字
                trigger: 'axis'
            },
            xAxis: [
                {  //x轴坐标数据
                    type: 'category',
                    data: that.data.warning_type
                },
            ],
            yAxis: [{   //y轴坐标数据
                type: 'value',
                minInterval: 1,
                max: 8,
            }],
            series: [  //驱动图表生成的数据内容数组，几条折现，数组中就会有几个对应对象，来表示对应的折线
                {
                    name: "value",
                    type: "bar",  //pie->饼状图  line->折线图  bar->柱状图
                    animation: false,
                    label: {normal: {show: true, position: "top", textStyle: {color: "#9EA7C4"}}},
                    color: function (params) {
                        if (params.dataIndex > 0)
                            return 'red';
                        else
                            return '#8cd5c2'
                    },
                    // itemStyle: {
                    //     normal: {
                    //         color:'#8cd5c2',
                    //     }
                    // },
                    data: that.data.warning_count,
                },
            ]
        };
        myCharts.setOption(options);
    }

    export default {
        mixins: [tableMixin],
        data() {
            return {
                columnsE: [
                    {
                        title: '机器ID',
                        field: 'machine_id',
                        formatter: (value, row) => {
                            return '<span class="ID">' + value + '</span>'
                        },
                        events: {
                            'click .ID': (e, value, row) => {
                                this.$router.push('/Detail/' + value);
                            }
                        }
                    },
                    {
                        field: 'loc',
                        title: '位置'
                    },
                    {
                        field: 'status',
                        title: '状态',
                        formatter:(value) =>{
                            return value==1?'异常':'正常'
                        },
                        cellStyle: (value, row, index, field) => {
                            if (value == 1){
                                return {
                                    css: {
                                        color: 'red'
                                    },
                                }
                            }
                            else
                            return {
                                    css: {
                                        color: 'green'
                                    },
                                }
                        },
                    },
                    {
                        field: 'predict_status',
                        title: '预测故障',
                        align: 'center',
                        cellStyle: (value, row, index, field) => {
                            if (value == 1){
                                return {
                                    css: {
                                        color: 'red'
                                    },
                                }
                            }
                            else
                            return {
                                    css: {
                                        color: 'green'
                                    },
                                }
                        },
                        formatter: (value, row) => {
                            if (value == true)
                                return '<span class="predict">' + '异常' + '</span>';
                            else
                                return '正常';
                        },
                        events: {
                            'click .predict': (e, value, row) =>{
                                this.$router.push('/exception/' + row.machine_id);
                            }
                        }

                    }
                ],
                data: [],
                optionsE: {
                    //showColumns: true,
                    pagination: true,
                    pageSize: 10,
                    height: 300,

                },
                columns: [
                    {
                        title: '机器ID',
                        field: 'machine_id',
                        formatter: (value, row) => {
                            return '<span class="ID">' + value + '</span>'
                        },
                        events: {
                            'click .ID': (e, value, row) => {
                                this.$router.push('/Detail/' + value);
                            }
                        }
                    }, {
                        field: 'cpu_util_percent',
                        title: 'CPU'
                    }, {
                        field: "disk_io_percent",
                        title: "磁盘"
                    },
                    {
                        field: 'loc',
                        title: '位置'
                    },
                    {
                        field: "mem_util_percent",
                        title: '内存'
                    }, {
                        field: "net_in",
                        title: '进网'
                    },
                    {
                        field: 'status',
                        title: '状态',
                        align: 'center',
                        formatter:(value) =>{
                            return value==1?'异常':'正常'
                        },
                        cellStyle: (value, row, index, field) => {
                            if (value == 1)
                                return {
                                    css: {
                                        color: 'red'
                                    }
                                }
                                else
                            return {
                                    css: {
                                        color: 'green'
                                    },
                                }
                        },
                    },
                    {
                        field: 'predict_status',
                        title: '预测故障',
                        align: 'center',
                        cellStyle: (value, row, index, field) => {
                            if (value == 1)
                                return {
                                    css: {
                                        color: 'red'
                                    }
                                }
                                else
                            return {
                                    css: {
                                        color: 'green'
                                    },
                                }
                        },
                        formatter: (value, row) => {
                            if (value == true)
                                return '<span class="predict">' + '异常' + '</span>';
                            else
                                return '正常';
                        },
                        events: {
                            'click .predict': (e, value, row) =>{
                                this.$router.push('/exception/' + row.machine_id);
                            }
                        }

                    },
                    {
                        field: 'time_stamp',
                        title: '时间'
                    }
                ],
                options: {
                    //showColumns: true,
                    pagination: true,
                    pageSize: 10,
                    width:300,
                }
            }
        },
        created() {
            getJson(this, "http://[2001:da8:270:2020:f816:3eff:fe20:a164]:8080/");
            this.intervalId = setInterval(() => {
                getJson(this,"http://[2001:da8:270:2020:f816:3eff:fe20:a164]:8080/")
            }, 3600)
        },
        mounted() {

        },
        methods: {
            clickRow(row) {
                alert(JSON.stringify(row))
            }
        }
    }
</script>

<style>
    .container {
        margin-top: 36px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;

    }
    .foot{
        width:90%;

    }

</style>
