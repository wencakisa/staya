<template>
  <div class="container">
    <section class="hero is-danger is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="box is-offset-3 is-6">
            <h3 class="title has-text-dark">Add Listing</h3>
            <form 
              method="post"
              @submit.prevent="geocode(location)">                
              <div class="field">
                <label 
                  class="label is-medium"
                  for="title">
                  Title
                </label>
                <div class="control">
                  <input
                    id="title"
                    v-model="title"
                    class="input is-medium"
                    type="text"
                    placeholder="Title"
                    required
                    autofocus="">
                </div>
              </div>

              <div class="field">
                <label 
                  class="label is-medium"
                  for="description">
                  Description
                </label>
                <div class="control">
                  <textarea
                    id="description"
                    v-model="description"
                    class="textarea is-medium"
                    type="textarea"
                    placeholder="Description"/>
                </div>
              </div>

              <div class="field">
                <label 
                  class="label is-medium"
                  for="price">
                  Price per night
                </label>
                <p class="control has-icons-left">
                  <input
                    id="price"
                    v-model="price"
                    class="input is-medium"
                    type="number"
                    step="0.01"
                    min="0.00"
                    required
                    placeholder="Price per night">
                  <span class="icon is-small is-left">
                    <i class="mdi mdi-currency-usd"/>
                  </span>
                </p>
              </div>

              <div class="field">
                <label 
                  class="label is-medium"
                  for="amenities">
                  Amenities
                </label>
                <div class="select is-fullwidth is-multiple">
                  <select multiple>
                    <option
                      v-for="amenity in amenities"
                      id="capitalize"
                      :key="amenity"
                      :value="amenity">{{ amenity }}</option>
                  </select>
                </div>
              </div>

              <div class="field">
                <label 
                  class="label is-medium"
                  for="location">
                  Location
                </label>
                <div class="control">
                  <input
                    id="title"
                    v-model="location.name"
                    class="input is-medium"
                    type="text"
                    required
                    placeholder="Location Address (ex. 1600 Amphitheatre Parkway, Mountain View, CA)">
                </div>
              </div>

              <button 
                type="submit"
                class="button is-block is-dark is-medium is-fullwidth">
                Add Listing
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  middleware: "auth",
  data() {
    return {
      apiKey: process.env.GEOCODE_API_KEY,
      amenities: [],
      address: '',
      location: {
        name: '',
        longtitude: null,
        latitude: null
      },
      price: null,
      description: '',
      title: ''
    };
  },
  mounted: function() {
    this.$axios.get("/amenities").then(res => {
      this.amenities = res.data;
    });
  },
  methods: {
    submit() {
      if (!$store.getters.isResident) {
        this.$axios.put('/auth/user', {
          is_resident: true
        }).then(() => {
          this.$store.commit('becomeResident')
          console.log(this.$store.getters.isResident)
        })
      }

      geocode()

      if (location.longtitude && location.latitude) {
        this.$axios.post('/listings', {
          amenities: this.amenities,
          location: this.location,
          price: this.price,
          description: this.description,
          title: this.title
        }).then(() => {
          this.$toasted.success("Added listing successfully!")
          this.$router.push('/listings')
        }).catch((error) => {
          this.$toasted.error(error.data.message)
        })
      }
    },
    geocode() {
      this.$axios
        .get(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(this.location.name)}&key=${this.apiKey}`)
        .then(res => {
          if (res.data.status === "ZERO_RESULTS") {
            this.$toasted.error("Could not find location's coordinates")
            return
          }
          this.location.longtitude = res.data.results[0].geometry.location.lng
          this.location.latitude = res.data.results[0].geometry.location.lat
        })

    }
  }
};
</script>

<style>
#capitalize:first-letter {
  text-transform: capitalize;
}
</style>
