<template>
  <div class="conteiner">
    <section class="hero is-danger is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-4 is-offset-4">
            <div class="box">
              <h3 class="title has-text-grey-dark">Login</h3>
              <p class="subtitle has-text-grey-dark">Please login to proceed.</p>
              <form 
                method="post"
                @submit.prevent="login">                
                <div class="field">
                  <div class="control">
                    <input 
                      v-model="username"
                      class="input is-large"
                      type="text"
                      placeholder="Username"
                      autofocus="">
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
                <button 
                  type="submit"
                  class="button is-block is-dark is-large is-fullwidth">
                  Login
                </button>
              </form>
              <br>
              <p class="has-text-grey">
                <nuxt-link to="/auth/register">Register</nuxt-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    login() {
      this.$auth.loginWith("local", {
        data: {
          username: this.username,
          password: this.password
        }
      }).then(res => {
        this.$toasted.success("Successfully Logged-In");
        this.$router.push("/")
      }).catch(e => {
        this.$toasted.error("Failed Logging In");
      });
    }
  },
  transition: 'bounce'
};
</script>

<style>
</style>