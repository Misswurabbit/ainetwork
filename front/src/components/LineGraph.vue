<template>
    <div>
        <div id="myCharts" ref="myCharts" :style="{height: '400px', width:'400px'}"></div>
    </div>

</template>

<script>
    function init(that){
        const myCharts = that.$echarts.init(that.$refs.myCharts);
        let c = that.$props.content;
        let options = {
            title: {
                text: c.name,   //图表顶部的标题
            },
            tooltip: {   //鼠标悬浮框的提示文字
                trigger: 'axis'
            },
            dataZoom: [{
                type: 'inside',
                // startValue: FFTData[0][0],
                start: 0,//百分比
                end: 100
            }, {
                start: 0,
                end: 100,
                handleSize: '100%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            xAxis: [
                {  //x轴坐标数据
                    type: 'value',
                    boundaryGap: false,
                    scale:true
                    //data: c.T
                },
                ],
            yAxis: [{   //y轴坐标数据
                type: 'value',
                axisLabel: {
                    formatter: '{value}'
                }
            }],
            series: [  //驱动图表生成的数据内容数组，几条折现，数组中就会有几个对应对象，来表示对应的折线
                {
                    name: "value",
                    type: "line",  //pie->饼状图  line->折线图  bar->柱状图
                    symbol: 'circle',     //设定为实心点
                    symbolSize: 3,   //设定实心点的大小
                    animation: false,
                    itemStyle: {
                        normal: {
                            color:'#8cd5c2',
                            lineStyle: {
                                color: '#8cd5c2' //改变折线颜色
                            }
                        }
                    },
                    data: c.TV,
                },
                {
                    name: "value",
                    type: "scatter",  //pie->饼状图  line->折线图  bar->柱状图
                    symbol: 'circle',     //设定为实心点
                    symbolSize: 5,   //设定实心点的大小
                    animation: false,
                    itemStyle: {
                        normal: {
                            color:'red',
                            // color: function (e) {
                            //     if (c.E[e.dataIndex] == 1) {
                            //         return 'red'
                            //     } else
                            //         return '#000'
                            // }, //改变折线点的颜色
                            lineStyle: {
                                color: '#8cd5c2' //改变折线颜色
                            }
                        }
                    },
                    data: c.TVE,
                },
            ]
        };
        myCharts.setOption(options);
    }
    export default {
        name: "LineGraph",
        props: {
            content: Object
        },
        mounted() {
            init(this)
         },
        watch:{
            'content':function(newVal){
                window.console.log('content trigger')
                init(this)
            }
        },
         methods:{
         }
    }
</script>

<style scoped>
    span{
        width:50%
    }
</style>
