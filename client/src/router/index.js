import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Catalog/Catalog.vue'
import Auth from "@/components/Auth/Auth";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/add',
        name: 'Add',
        component: () => import(/* webpackChunkName: "add" */ '../components/Catalog/CatalogAdd.vue')
    },
    {
        path: '/auth',
        name: 'Auth',
        component: Auth
    },
    {
        path: '/profile/:id',
        name: 'Profile',
        component: () => import(/* webpackChunkName: "add" */ '../components/Profile/Profile.vue')
    },
    {
        path: '/edit/:id',
        name: 'Edit',
        component: () => import(/* webpackChunkName: "add" */ '../components/Catalog/CatalogEdit.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
