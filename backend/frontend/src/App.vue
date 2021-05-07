<template>
    <div id="app">
        <router-view name="header"></router-view>
        <v-fade-transition mode="out-in">
          <main>
            <router-view></router-view> 
          </main>
        </v-fade-transition>
    </div>
</template>
<script>
// import { FadeTransition } from "vue2-transitions";
// import Navbar from "@/components/Navbar"
export default {
  components: {
    // Navbar,
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
  /* font-size:1.3em; */
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
