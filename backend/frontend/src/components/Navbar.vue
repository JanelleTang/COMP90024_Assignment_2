<template>
    <div id="nav-toolbar">
        <v-app-bar
        dense
        dark
        absolute
        clipped-left
        app
        hide-on-scroll
        scroll-target="#scrolling-techniques-4"
        >
            <v-menu v-if="$vuetify.breakpoint.mdAndDown">
                <template v-slot:activator="{ on }">
                <v-btn icon v-on="on">
                    <v-app-bar-nav-icon ></v-app-bar-nav-icon>
                </v-btn>
                </template>

                <v-list>
                <v-list-item v-if="activeUser" to="create">
                    <v-list-item-title>Create Post</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="activeUser" to="/">
                    <v-list-item-title>All Posts</v-list-item-title>
                </v-list-item>
                </v-list>
            </v-menu>
        
            <v-toolbar-title class="pr-3">
                <v-btn to="/">
                    <v-list-item-avatar>
                        <v-img :src=logo></v-img>
                    </v-list-item-avatar>
                </v-btn>
                Project Title
            </v-toolbar-title>
            <v-toolbar-item class="mx-3 d-none d-lg-block">
                <v-btn
                class="nav-btn"
                text
                depressed
                v-for="item in nav_items"
                :key="item.name"
                :to="item.href"
                >
                <v-icon class="pr-1">{{item.icon}}</v-icon>
                {{ item.title }}
                </v-btn>
            </v-toolbar-item>
            <v-spacer></v-spacer>
            <v-bottom-sheet>
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                    dark
                    v-bind="attrs"
                    v-on="on"
                    icon
                    >
                        <v-icon>mdi-account-multiple</v-icon>
                     </v-btn>
                </template>
            <v-sheet
                class="text-center" id="name-sheet"
                :height="$vuetify.breakpoint.xs ? 450 : '230'"
            >
                <v-btn
                icon
                class="mt-6"
                text
                color="error"
                @click="sheet = !sheet"
                >
                    <v-icon>mdi-close</v-icon>
                </v-btn>
                <div class="my-3 mx-5">
                    <v-row no-gutters>
                        <v-col class=".d-sm-none .d-md-flex" cols="1"></v-col>
                        <v-col
                        sm="4"
                        md="2"
                        cols="12"
                        v-for="person in names"
                        :key="person.name"
                        >
                            <v-list-item two-line class="px-2 py-0 ml-n10" id="sidebar-names">
                                <v-list-item-icon>
                                    <v-icon></v-icon>
                                </v-list-item-icon>
                                <v-list-item-content>
                                <v-list-item-title>{{ person.name }}</v-list-item-title>
                                <v-list-item-subtitle>{{ person.id }}</v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                        </v-col>
                        <v-col class=".d-sm-none .d-md-flex" cols="1"></v-col>
                    </v-row>
                </div>
            </v-sheet>

            </v-bottom-sheet>

            
            
        </v-app-bar>
    
        <v-content>

        </v-content>
    </div>
</template>
<script>
  export default {
    data: () => ({
      sheet: false,
      nav_items: [
          { title: 'Map Overview', icon: 'mdi-map-legend', href: '/map' },
          { title: 'Dashboard', icon: 'mdi-view-dashboard', href: '/dashboard'},
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
        logo: require("@/assets/global-warming.png"),
    }),
  }
</script>

<style>
/* Can't remove hover underline in navbar */
.nav-btn a:hover{
    text-decoration: none!important;
}

.name-sheet {
    position: static;
}

</style>