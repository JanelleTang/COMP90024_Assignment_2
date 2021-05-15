<template>
  <div class="ma-12 pa-12">
        <v-navigation-drawer 
            v-model="drawer" 
            :width="250"
            permanent
            expand-on-hover
            bottom
            app
            clipped
            >
            <v-list>
            <v-list-item class="px-2">
                <v-list-item-icon class="pl-2">
                    <v-icon>
                        mdi-dots-vertical-circle-outline
                    </v-icon>
                </v-list-item-icon>
                <v-list-item-title class="title">Options</v-list-item-title>
            </v-list-item>
            </v-list>

            <v-list nav dense>
            <v-list-item
            link
            v-for="item in nav_items"
            :key="item.name"
            >
            <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
                
                <button :id="item.id">{{ item.text }}</button>
            </v-list-item-content>
            </v-list-item>
        </v-list>
        <v-divider></v-divider>
        </v-navigation-drawer>
    </div>
</template>


<script>
  export default {
    data () {
      return {
        drawer: true,
        nav_items: [
          { text: 'Australia', icon: 'mdi-card-search', id: 'fit-au' },
          { text: 'Victoria', icon: '', id: 'fit-vic'},
          { text: 'NSW', icon: '', id: 'fit-nsw'},
        ],
        mini: true,
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