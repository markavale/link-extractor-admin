(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["about"],{"4ffd":function(t,a,e){t.exports=e.p+"static/img/logo.c2162052.png"},"710f":function(t,a,e){},"9dcd":function(t,a,e){"use strict";var n=e("710f"),s=e.n(n);s.a},d178:function(t,a,e){"use strict";var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{attrs:{id:"nav"}},[e("nav",{staticClass:"navbar navbar-b navbar-expand-md fixed-top",class:[t.is_transparent?"navbar-trans":"navbar-reduce"],attrs:{id:"mainNav"},on:{scroll:function(a){return a.preventDefault(),t.onScroll(a)}}},[e("div",{staticClass:"container"},[t._m(0),t._m(1),e("div",{staticClass:"navbar-collapse collapse justify-content-end",attrs:{id:"navbarDefault"}},[e("ul",{staticClass:"navbar-nav"},[e("li",{staticClass:"nav-item"},[e("a",{staticClass:"nav-link js-scroll",attrs:{href:"#"}},[t._v("Welcome, "+t._s(t.user.username))])]),t.isAuthenticated?t._e():e("li",{staticClass:"nav-item"},[e("router-link",{staticClass:"nav-link",attrs:{to:{name:"login"}}},[t._v("Login")])],1),t.isAuthenticated?e("li",{staticClass:"nav-item"},[e("router-link",{staticClass:"nav-link",attrs:{to:{name:"logout"}}},[t._v("Logout")])],1):t._e()])])])])])},s=[function(){var t=this,a=t.$createElement,n=t._self._c||a;return n("a",{staticClass:"navbar-brand js-scroll",attrs:{href:"/"}},[n("img",{staticClass:"logo",attrs:{src:e("4ffd"),alt:"Logo"}}),t._v(" MAV ")])},function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("button",{staticClass:"navbar-toggler collapsed",attrs:{type:"button","data-toggle":"collapse","data-target":"#navbarDefault","aria-controls":"navbarDefault","aria-expanded":"false","aria-label":"Toggle navigation"}},[e("span"),e("span"),e("span")])}],r=e("5530"),o=e("2f62"),i=e("5834"),l={data:function(){return{drawer:!1,group:null,user:{},is_transparent:!0}},computed:Object(r["a"])(Object(r["a"])({},Object(o["b"])(["isAuthenticated"])),{},{currentUser:function(){if(this.isAuthenticated){var t=this.$store.state.user.user;return t}var a={username:"None"};return a}}),mounted:function(){window.addEventListener("scroll",this.onScroll),this.getCurrentUser()},beforeDestroy:function(){window.removeEventListener("scroll",this.onScroll)},created:function(){this.getCurrentUser()},methods:{onScroll:function(t){this.is_transparent=!(t.target.documentElement.scrollTop>0)},getCurrentUser:function(){var t=this;this.isAuthenticated&&i["a"].get("auth/user/",{headers:{"Content-Type":"application/x-www-form-urlencoded",Authorization:"Token ".concat(localStorage.getItem("token"))}}).then((function(a){t.$store.commit("currentUser",a.data),t.user=t.$store.state.user.user,console.log("User")})).catch((function(t){return console.log(t)}))}}},c=l,u=(e("9dcd"),e("2877")),d=Object(u["a"])(c,n,s,!1,null,"01c393f2",null);a["a"]=d.exports},f820:function(t,a,e){"use strict";e.r(a);var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"about"},[e("Navbar"),e("h1",[t._v("This is an about page")])],1)},s=[],r=e("d178"),o={name:"About",components:{Navbar:r["a"]}},i=o,l=e("2877"),c=Object(l["a"])(i,n,s,!1,null,null,null);a["default"]=c.exports}}]);
//# sourceMappingURL=about.99772e6b.js.map