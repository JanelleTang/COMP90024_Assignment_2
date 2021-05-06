<template>
  <div class="ma-12 pa-12 test">
      <v-app>
        <v-navigation-drawer 
        v-model="drawer" 
        :width="250"
        app permanent
        expand-on-hover
        bottom
        >
            <v-list>
            <v-list-item class="px-2">
                <v-list-item-avatar>
                <v-img :src=logo></v-img>
                </v-list-item-avatar>
                <v-list-item-title class="title"><h3>Project Name</h3></v-list-item-title>
            </v-list-item>

            </v-list>

            <v-divider></v-divider>

            <v-list nav dense>
            <v-list-item
            v-for="item in menu_items"
            :key="item.title"
            :href="item.href"
            link
            >
            <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
                <router-link to= "dashboard/">{{ item.title }}</router-link>
            </v-list-item-content>
            </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-container id="sidebar-footer">
        <v-list class="py-0"
        v-for="item in names"
        :key="item.name"
        >
            <v-list-item two-line class="px-2 py-0 my-0" id="sidebar-names">
                <v-list-item-icon>
                    <v-icon></v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.id }}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>

        </v-list>
</v-container>  
        </v-navigation-drawer>
        <v-content>
            <v-fade-transition mode="out-in">
                <router-view></router-view>
            </v-fade-transition>
        </v-content>
      </v-app>
  </div>
</template>


<script>
  export default {
    data () {
      return {
        drawer: true,
        menu_items: [
          { title: 'Map Overview', icon: 'mdi-map-legend', href: 'dashboard/' },
          { title: 'Dashboard', icon: 'mdi-view-dashboard', href: 'map/'},
          { title: 'Information', icon: 'mdi-folder-information', },
        ],
        names: [
            {name: 'Janelle Tang', id: '694209'},
            // INSERT YOUR NAMES WITH THE FOLLOWING TEMPLATE 
            {name: 'NAME', id: 'STUDENTID'},
            {name: 'NAME', id: 'STUDENTID'},
            {name: 'NAME', id: 'STUDENTID'},
            {name: 'NAME', id: 'STUDENTID'},
        ],
        mini: true,
        logo: require("@/assets/global-warming.png")
      }
    },
  }
</script>

<style>
#sidebar-footer {
    position: relative;
    padding-bottom: 10px;
    position: absolute;
    bottom: 0;
}

</style>