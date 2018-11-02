<template>
  <nav 
    class="navbar is-dark"
    role="navigation"
    aria-label="main navigation">
    <div class="navbar-brand">
      <nuxt-link 
        class="navbar-item has-text-weight-bold" 
        to="/">
        staya
      </nuxt-link>

      <a
        :class="{ 'is-active': isMenuActive }"
        role="button"
        class="navbar-burger burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbarBasicExample"
        @click="toggleMenu('isMenuActive')">
        <span aria-hidden="true"/>
        <span aria-hidden="true"/>
        <span aria-hidden="true"/>
      </a>
    </div>

    <div 
      id="navbarBasicExample"
      :class="{ 'is-active': isMenuActive }"
      class="navbar-menu">
      <div class="navbar-start">
        <a
          href="/listings"
          class="navbar-item">
          Listings
        </a>
      </div>

      <div
        v-if="!this.$auth.loggedIn"
        class="navbar-end">
        <nuxt-link
          to="/auth/register"
          class="navbar-item">
          Register
        </nuxt-link>
        <nuxt-link 
          to="/auth/login"
          class="navbar-item">
          Log in
        </nuxt-link>
      </div>
      <div 
        v-else
        class="navbar-item">
        <div class="navbar-item has-dropdown is-hoverable">
          <a
            id="username" 
            class="navbar-link is-white">
            {{ $auth.user.username }}
          </a>

          <div class="navbar-dropdown is-right">
            <a
              v-if="!$store.getters.isResident"
              class="navbar-item">
              Become resident
            </a>
            <nuxt-link 
              :to="`/users/${$auth.user.username}`" 
              class="navbar-item">
              My Profile
            </nuxt-link>
            <a 
              v-if="$store.getters.isResident"
              :href="`/listings?search=${$auth.user.username}`" 
              class="navbar-item">
              My Listings
            </a>
            <hr class="navbar-divider">
            <a 
              class="navbar-item"
              @click="$auth.logout()">
              Logout
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>

</template>

<script>
import AddListing from "~/components/AddListing.vue";

export default {
  components: {
    AddListing
  },

  data() {
    return {
      isMenuActive: false,
      isModalActive: false
    };
  },

  methods: {
    toggleMenu: function(prop) {
      this.$data[prop] = !this.$data[prop];
    }
  },

  transition: 'bounce'
};
</script>

<style>
  #username {
    color: white !important;
  }
</style>