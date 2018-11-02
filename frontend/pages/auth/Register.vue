<template>
  <section class="hero is-danger is-fullheight-with-navbar">
    <div class="container has-text-centered">
      <div class="column is-6 is-offset-3">
        <div class="box">
          <h3 class="title has-text-grey-dark">Register</h3>
          <p class="subtitle has-text-grey-dark">Create new account.</p>
          <form 
            method="post"
            @submit.prevent="register">
            <div class="field">
              <div class="control">
                <input 
                  v-validate="'required|email'"
                  v-model="email"
                  class="input is-large"
                  type="email"
                  placeholder="Email"
                  autofocus="">
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input 
                  v-model="username"
                  class="input is-large"
                  type="text"
                  placeholder="Username">
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input 
                  v-model="password"
                  class="input is-large"
                  type="password"
                  placeholder="Password">
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input 
                  v-model="confirmPassword"
                  class="input is-large"
                  type="password"
                  placeholder="Confirm password">
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input 
                  v-model="firstName"
                  class="input is-large"
                  type="text"
                  placeholder="First name">
              </div>
            </div>

            <div class="field">
              <div class="control">
                <input 
                  v-model="lastName"
                  class="input is-large"
                  type="text"
                  placeholder="Last name">
              </div>
            </div>
            <!-- <div class="field">
              <input 
                id="visitor"
                v-model="isResident" 
                :value="false"
                class="is-checkradio is-black"
                type="radio"
                name="radioInline">
              <label for="visitor">Visitor</label>
              <input
                id="resident"
                v-model="isResident" 
                :value="true"
                class="is-checkradio is-black"
                type="radio"
                name="radioInline">
              <label for="resident">Resident</label>
            </div> -->
            <button 
              type="submit"
              class="button is-block is-dark is-large is-fullwidth">
              Register
            </button>
          </form>
          <br>
          <p class="has-text-grey">
            <nuxt-link to="/auth/login">Login</nuxt-link>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      confirmPassword: "",
      firstName: "",
      lastName: "",
      // isResident: false
    };
  },
  methods: {
    async register() {
      try {
        await this.$axios.post('/auth/registration/', {
          email: this.email,
          username: this.username,
          password1: this.password,
          password2: this.confirmPassword,
          first_name: this.firstName,
          last_name: this.lastName,
          // is_resident: this.isResident
        })

        await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password
          },
        })
        this.$toasted.success("Successfully Registered");
        this.$router.push('/')
      } catch (e) {
        this.$toasted.error(JSON.stringify(e.response.data));
        this.error = e.response.data.message
      }
    }
  },
  transition: 'bounce'
}
</script>

<style>

</style>
