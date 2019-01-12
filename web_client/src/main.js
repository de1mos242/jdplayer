import Vue from 'vue'
import App from './App.vue'
import store from './store'
import VueRouter from "vue-router";
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios';
import {isUndefined} from "vue-authenticate/src/utils";
import VueAxios from "vue-axios";


Vue.config.productionTip = false

axios.defaults.baseURL = '/api';

export function getRedirectUri(uri) {
    try {
        return (!isUndefined(uri))
            ? `${window.location.origin}${uri}`
            : window.location.origin
    } catch (e) {
        alert(`we have problem: ${e}`)
    }

    return uri || null;
}


Vue.use(VueRouter)
Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
    tokenName: 'access_token',
    baseUrl: '',
    storageType: 'cookieStorage',
    providers: {
        facebook: {
            name: 'facebook',
            clientId: '1891789847745371',
            url: '/auth/facebook',
            authorizationEndpoint: 'https://www.facebook.com/v2.5/dialog/oauth',
            redirectUri: getRedirectUri('/'),
            requiredUrlParams: ['display', 'scope'],
            scope: ['email'],
            scopeDelimiter: ',',
            display: 'popup',
            oauthType: '2.0',
            popupOptions: {width: 580, height: 400}
        },
        vk: {
            name: 'vk',
            clientId: '3380204',
            url: '/auth/vk',
            authorizationEndpoint: 'https://oauth.vk.com/authorize',
            redirectUri: getRedirectUri('/'),
            requiredUrlParams: ['display', 'scope'],
            scope: ['audio'],
            scopeDelimiter: ',',
            display: 'popup',
            oauthType: '2.0',
            popupOptions: {width: 580, height: 400}
        },
    }
})

var router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'index',
            component: {
                data: function () {
                    return {
                        access_token: null,
                        response: null
                    }
                },
                template: `
          <div class="index-component">
            <div class="authentication-status" v-if="$auth.isAuthenticated()">
              You are successfully authenticated
              <div class="authentication-status__token">{{$auth.getToken()}}</div>
            </div>
            <button @click="authLogin()">Login</button>
            <button @click="authRegister()">Register</button>
            <button @click="authLogout()">Logout</button>
            
            <hr />
            <button @click="auth('github')" class="button--github">Auth github</button>
            <button @click="auth('facebook')" class="button--facebook">Auth facebook</button>
            <button @click="auth('google')" class="button--google">Auth google</button>
            <button @click="auth('twitter')" class="button--twitter">Auth twitter</button>
            <hr />
            
            <button @click="auth('instagram')" class="button--instagram">Auth instagram</button>
            <button @click="auth('bitbucket')" class="button--bitbucket">Auth bitbucket</button>
            <button @click="auth('linkedin')" class="button--linkedin">Auth LinkedIn</button>
            <button @click="auth('vk')" class="button--vk">Auth VK</button>
            <pre class="response" v-if="response !== null">{{JSON.stringify(response, null, 2)}}</pre>
          </div>
        `,
                methods: {

                    authLogin: function () {
                        var this_ = this;
                        let user = {
                            email: 'john.doe@domain.com',
                            password: 'pass123456'
                        };

                        if (this.$auth.isAuthenticated()) {
                            this.$auth.logout()
                        }

                        this.$auth.login(user).then(function (response) {
                            this_.response = response
                        })
                    },

                    authRegister: function () {
                        var this_ = this;
                        let user = {
                            name: 'John Doe',
                            email: 'john.doe@domain.com',
                            password: 'pass123456'
                        };

                        if (this.$auth.isAuthenticated()) {
                            this.$auth.logout()
                        }

                        this.$auth.register(user).then(function (response) {
                            this_.response = response
                        })
                    },

                    authLogout: function () {
                        this.$auth.logout().then(() => {
                            if (!this.$auth.isAuthenticated()) {
                                this.response = null
                            }
                        })
                    },

                    auth: function (provider) {
                        if (this.$auth.isAuthenticated()) {
                            this.$auth.logout()
                        }

                        this.response = null

                        var this_ = this;
                        this.$auth.authenticate(provider).then(function (authResponse) {
                            if (provider === 'github') {
                                this_.$http.get('https://api.github.com/user').then(function (response) {
                                    this_.response = response
                                })
                            } else if (provider === 'facebook') {
                                this_.$http.get('https://graph.facebook.com/v2.5/me', {
                                    params: {access_token: this_.$auth.getToken()}
                                }).then(function (response) {
                                    this_.response = response
                                })
                            } else if (provider === 'google') {
                                this_.$http.get('https://www.googleapis.com/plus/v1/people/me/openIdConnect').then(function (response) {
                                    this_.response = response
                                })
                            } else if (provider === 'twitter') {
                                this_.response = authResponse.body.profile
                            } else if (provider === 'instagram') {
                                this_.response = authResponse
                            } else if (provider === 'bitbucket') {
                                this_.$http.get('https://api.bitbucket.org/2.0/user').then(function (response) {
                                    this_.response = response
                                })
                            } else if (provider === 'linkedin') {
                                this_.response = authResponse
                            } else if (provider === 'live') {
                                this_.response = authResponse
                            }
                        }).catch(function (err) {
                            this_.response = err
                        })
                    }
                }
            }
        },

        {
            path: '/auth/callback',
            component: {
                template: '<div class="auth-component"></div>'
            }
        }
    ]
})

new Vue({
    store,
    router,
    render: h => h(App)
}).$mount('#app')
