<template>
  <div class="home" id = "background-wrapper">
    <!-- <Navbar></Navbar> -->
    <v-app>
        <v-parallax id="parallax-home"
          light
          height="780"
          src="https://images.unsplash.com/photo-1569060368645-4ab30c8d8b0e?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80"
        >
      <v-content>
        <v-container id = "home-container">
          <h1>Understanding Attitudes to Climate Change Through Demographic Data</h1>
          <br/>
          <div class="box">Click the button below to get started!</div>  
        </v-container>
        
      </v-content>
      <v-fab-transition>
        <v-btn id="start-btn"
        color="light-blue"
        elevation="5"
        fab
        x-large
        href="/map"
        >
          <v-icon color="white">mdi-navigation</v-icon>
        </v-btn>
      </v-fab-transition>
      </v-parallax>
    </v-app>
  </div>
</template>

<script>
// import Navbar from "@/components/Navbar.vue";
export default {
  name: "Home",
  components: {
  },
};
</script>

<style>
.home{
  height:90vh;
}
#parallax-home{
  padding-top: 10px;
  bottom:0;
}

#home-container {
  color: #fff;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
}

#background-wrapper {
  background-size: cover;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  background-size: cover;
  -o-background-size: cover;
  z-index:1 
}

#start-btn {
  animation: MoveUpDown 1.1s linear infinite;
  position: fixed;
  top: 40%;
  left: 50%;
  /* bring your own prefixes */
  transform: translate(-50%, -50%);
  text-decoration: none;
}

@keyframes MoveUpDown {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

</style>