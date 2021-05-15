import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import Map from '@/views/Map.vue'
import Dashboard from '@/views/Dashboard.vue'
import Navbar from "@/components/Navbar";
Vue.use(Router)

export default new Router({
    mode: 'history',
    // base: process.env.BASE_URL,

    routes: [

        {
        path: '/',
        name: 'Home',
        components: {
            header: Navbar,
            default: Home,
        }
        },
        {
            path: '/map',
            name: 'Map',
            components: {
                header: Navbar,
                default: Map,
            }
        },
        {
        path: '/dashboard',
        name: 'Dashboard',
        components: {
            header: Navbar,
            default: Dashboard,
        }
        },
    ]
})