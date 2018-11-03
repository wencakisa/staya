<template>
  <div class="container">
    <section class="hero is-danger is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-8 is-offset-2">
            <div class="box">
              <h3 class="title has-text-grey-dark">Book a room or apartment</h3>
              <section class="form">
                <div class="field">
                  <div class="control">
                    <input 
                      v-model="city"
                      class="input is-large"
                      type="text"
                      placeholder="City"
                      autofocus="">
                  </div>
                </div>
    
                <b-field>
                  <b-datepicker
                    v-model="checkInDate"
                    :min-date="checkInMinDate"
                    name="checkInDate"
                    placeholder="Check in"
                    icon="calendar-today"
                    editable/>
                  
                </b-field>
                <b-field>
                  <b-datepicker
                    v-model="checkOutDate"
                    :min-date="checkOutMinDate"
                    name="checkOutDate"
                    placeholder="Check out"
                    icon="calendar-today" />
                </b-field>
                <button 
                  class="button is-block is-dark is-large is-fullwidth"
                  @click="search">
                  <span class="mdi mdi-magnify"/>
                  Search
                </button>
              </section>
              <br>
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
    const today = new Date();
    return {
      city: "",
      checkInDate: null,
      checkOutDate: null,
      checkInMinDate: new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate()
      ),
      checkOutMinDate: new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate() + 1
      )
    };
  },
  methods: {
    search() {
      this.$validator.validateAll().then(result => {
        if (result) {
          this.$router.push(`/listings?search=${this.city}`)
          return;
        }
        this.$toasted.error("Correct them errors!");
      });
    }
  },
  transition: "bounce"
};
</script>

<style>
</style>