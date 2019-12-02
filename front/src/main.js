import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App.vue'
import router from './router'
import echarts from 'echarts'
import ElementUI from 'element-ui';

Vue.use(BootstrapVue)
Vue.use(ElementUI);

import './plugins/table.js'

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

new Vue({
    render: h => h(App),
    router
}).$mount('#app')
