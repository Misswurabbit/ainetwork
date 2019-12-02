<template>
  <div>
    <div class="top">
    <img src="./assets/moniter.png">
      <h2>数据监控平台</h2>
    </div>
    <router-view />
  </div>
</template>
<script>

export default {
  name: 'app',
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
  .top{
    width: 80%;
    margin-left: 10%;
    border-bottom:2px solid grey;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    display:flex;
    flex-direction: row;
    align-items:center;
  }
  .top img{
    width:64px;
    height:64px;
  }
</style>
