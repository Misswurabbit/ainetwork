module.exports = {
  configureWebpack: {
    //host: '2001:da8:270:2020:f816:3eff:fe20:a164',
    //port: 8080,
    resolve: {
      alias: {
        vue$: 'vue/dist/vue.esm.js'
      }
    }
  },
  devServer: {
	host: '2001:da8:270:2020:f816:3eff:fe20:a164',
  	port: 5903,
  }
}
