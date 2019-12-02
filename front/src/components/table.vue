<template>
    <div>
        <v-table
                is-vertical-resize
                :vertical-resize-offset='60'
                is-horizontal-resize
                style="width:100%"
                :multiple-sort="false"
                :min-height="350"
                even-bg-color="#f2f2f2"
                :title-rows="tableConfig.titleRows"
                :columns="tableConfig.columns"
                :table-data="tableConfig.tableData"
                row-hover-color="#eee"
                row-click-color="#edf7ff"
                @sort-change="sortChange"
                :paging-index="(pageIndex-1)*pageSize"
        ></v-table>

        <div class="mt20 mb20 bold"></div>
        <v-pagination @page-change="pageChange" @page-size-change="pageSizeChange" :total="total" :page-size="pageSize" :layout="['total', 'prev', 'pager', 'next', 'sizer', 'jumper']"></v-pagination>
    </div>
</template>

<style>
    .title-cell-class-name-test1 {
        background-color: #2db7f5;
        color:#fff;
    }
    .title-cell-class-name-test2 {
        background-color: #f60;
        color:#fff;
    }
</style>

<script>

    //import tableDate from '../../../1.json'
    export default{
        props:{
          tableDate:[]
        },
        data(){
            return {
                pageIndex:1,
                pageSize:50,
                total:this.$props.tableDate.length,
                tableConfig: {
                    multipleSort: false,
                    tableData: [],
                    columns: [
                        {
                            field: 'id', width: 50, titleAlign: 'center', columnAlign: 'center',
                            formatter: function (rowData, index,pagingIndex) {
                                var currentIndex = index+pagingIndex;
                                //return currentIndex < 3 ? '<span style="color:red;font-weight: bold;">' + (currentIndex + 1) + '</span>' : currentIndex + 1
                                return currentIndex + 1
                            },
                            isFrozen: true
                        },

                        {field:'cpu_util_percent',width: 100, columnAlign:'center', isFrozen:false,isResize:true},
                        {field: 'disk_io_percent', width: 100, columnAlign: 'center', isFrozen: false,isResize:true},
                        {field: 'machine_id', width: 100, columnAlign: 'center', isFrozen: false},
                        {field: 'mem_gps', width: 100, columnAlign: 'center', isFrozen: false,},
                        {field: 'mem_util_percent', width: 100, columnAlign: 'center',isResize:true},
                        {field: 'mkpi', width: 100, columnAlign: 'center'},
                        {field: 'net_in', width: 50, columnAlign: 'center',isResize:true},
                        {field: 'net_out', width: 50, columnAlign: 'center',isResize:true},
                        {field: 'time_stamp', width: 100, columnAlign: 'center',isResize:true}


                    ],
                    titleRows: [
                        [   {fields:['id'], title:'序号',titleAlign:'center'},
                            {fields:['cpu_util_percent'], title:'cpu_util_percent(%)',titleAlign:'center'},
                            {fields:['disk_io_percent'], title:'disk_io_percent(%)',titleAlign:'center'},
                            {fields:['machine_id'], title:'machine_id',titleAlign:'center'},
                            {fields:['mem_gps'], title:'mem_gps',titleAlign:'center'},
                            {fields:['mem_util_percent'], title:'mem_util_percent(%)',titleAlign:'center'},
                            {fields:['mkpi'], title:'mkpi',titleAlign:'center'},
                            {fields:['net_in'], title:'net_in',titleAlign:'center'},
                            {fields:['net_out'], title:'net_out',titleAlign:'center'},
                            {fields:['time_stamp'], title:'time_stamp',titleAlign:'center'}
                        ]

                    ],
                }
            }
        },
        watch:{
            'tableDate':function (oldVal,newVal){
                window.console.log(oldVal,newVal)
                this.getTableData();
            }
        },
        methods:{
            getTableData(){
                this.tableConfig.tableData = this.$props.tableDate.slice((this.pageIndex-1)*this.pageSize,(this.pageIndex)*this.pageSize)
            },
            pageChange(pageIndex){
                this.pageIndex = pageIndex;
                this.getTableData();
                window.console.log(pageIndex)
            },
            pageSizeChange(pageSize){
                this.pageIndex = 1;
                this.pageSize = pageSize;
                this.getTableData();
            },
            sortChange(params){
                if (params.height.length > 0){

                    this.tableConfig.tableData.sort(function (a, b) {

                        if (params.height === 'asc'){

                            return a.height - b.height;
                        }else if(params.height === 'desc'){

                            return b.height - a.height;
                        }else{

                            return 0;
                        }
                    });
                }
            },
        },
        created(){
            this.getTableData();
        }
    }
</script>
