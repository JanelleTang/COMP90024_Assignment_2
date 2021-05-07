<template>
  <div class="home" id = "background-wrapper">
    <!-- <Navbar></Navbar> -->
    <v-app>
      <v-content>
        <v-container>
          Click the button below to get started!        
        </v-container>

      </v-content>
      <v-container>
          Click the button below to get started!        
        </v-container>
      <v-fab-transition>
        <v-btn id="start-btn"
        color="light-blue"
        elevation="5"
        fab
        x-large
        href="dashboard/"
        >
          <v-icon color="white">mdi-navigation</v-icon>
        </v-btn>
      </v-fab-transition>
    </v-app>
  </div>
</template>

<script>
// import Navbar from "@/components/Navbar.vue";

export default {
  name: "Home",
  components: {
    // Navbar
  },
};
</script>

<style>
.home{
  height:100vh
}
/* #background-wrapper {
        background:linear-gradient(0deg, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.7)), url(../assets/abstract_low_poly_elegant_banner_design_0111.jpg);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        background-size: cover;
        -o-background-size: cover;
        z-index:1
    } */
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