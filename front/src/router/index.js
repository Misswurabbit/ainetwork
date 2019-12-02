import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/Home.vue'
import Detail from '@/components/Detail.vue'
import Exception from "@/components/Exception.vue"

Vue.use(Router)

export default new Router({
    routes:[{
        path:'/',
        name:'home',
        component:HelloWorld
    },
        {
            path:'/detail/:id',
            props:true,
            name:'detail',
            component:Detail
        },
        {
            path:'/exception/:id',
            props:true,
            name:'exception',
            component:Exception
        }
    ]
})