<template>
    <div id="app">
        <Sidebar></Sidebar>
        <v-content>
          <router-view></router-view>
        </v-content>
    </div>
</template>
<script>
// import { FadeTransition } from "vue2-transitions";
import Sidebar from "@/components/Sidebar"
export default {
  components: {
    Sidebar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
