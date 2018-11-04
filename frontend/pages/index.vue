<template>
  <div class="container">
    <section class="hero is-danger is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="column is-8 is-offset-2">
            <div class="box">
              <h3 class="title has-text-grey-dark">Book a room or apartment</h3>
              <form class="form" @submit.prevent="doSearch">
                <div class="field">
                  <div class="control">
                    <input 
                      v-model="search"
                      class="input is-large"
                      type="text"
                      placeholder="City"
                      autofocus="">
                  </div>
                </div>
    
                <b-field>
                  <b-datepicker
                    v-model="checkInDate"
                    :min-date="minCheckInDate"
                    name="checkInDate"
                    @input="setMinCheckOutDate(checkInDate)"
                    placeholder="Check in"
                    icon="calendar-today"
                    editable/>
                  
                </b-field>
                <b-field>
                  <b-datepicker
                    v-model="checkOutDate"
                    :min-date="minCheckOutDate"
                    name="checkOutDate"
                    placeholder="Check out"
                    icon="calendar-today" />
                </b-field>
                <button class="button is-block is-dark is-large is-fullwidth">
                  <span class="mdi mdi-magnify"/>
                  Search
                </button>
              </form>
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
      search: "",
      checkInDate: null,
      checkOutDate: null,
      minCheckInDate: new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate()
      ),
      minCheckOutDate: new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate() + 1
      )
    };
  },
  methods: {
    doSearch() {
      let url = new URL(`${window.location.href}listings`);
      console.log(url)
      if (this.search) {
        url.searchParams.append("search", this.search);
      }
      if (this.checkInDate) {
        url.searchParams.append("free_from", this.$moment(this.checkInDate).format('YYYY-MM-DD'));
      }
      if (this.checkOutDate) {
        url.searchParams.append("free_to", this.$moment(this.checkOutDate).format('YYYY-MM-DD'));
      }
      window.location.href = url;
    },
    setMinCheckOutDate(checkInDate) {
      var result = new Date(checkInDate);
      result.setDate(result.getDate() + 1);
      this.minCheckOutDate = result;
    }
  },
  transition: "bounce"
};
</script>

<style>
</style>