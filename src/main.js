import Vue from "vue";
import App from "./App.vue";
import store from "./store/store";
import router from "./router";
import vuetify from "./plugins/vuetify";
import CxltToastr from 'cxlt-vue2-toastr'
import moment from "moment"
import JsonExcel from "vue-json-excel";

Vue.component("downloadExcel", JsonExcel);
Vue.use(CxltToastr)


Vue.config.productionTip = false;
Vue.filter('formatDate', function(value) {
    if (value) {
        // return moment(String(value)).format('MM/DD/YYYY hh:mm')
        return moment(String(value)).format('LLL')
    }
});
// Vue router validation
router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    next()
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!store.getters.isAuthenticated) {
            next({
                name: "login",
                query: { redirect: to.fullPath }
            });
        } else {
            next();
        }
    } else if (to.matched.some((record) => record.meta.requiresLogged)) {
        if (store.getters.isAuthenticated) {
            next({
                path: "/",
            });
        } else {
            next();
        }
    } else {
        next();
    }
});
new Vue({
    router,
    store,
    vuetify,
    render: (h) => h(App),
}).$mount("#app");