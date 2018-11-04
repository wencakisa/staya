<template>
  <div class="container">
    <section class="hero is-danger is-fullheight-with-navbar">
      <div class="hero-body">
        <div class="container has-text-centered">
          <div class="box is-offset-3 is-6">
            <h3 class="title has-text-dark">Add Listing</h3>
            <form 
              method="post"
              @submit.prevent="submit">                
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
                  for="guests">
                  Guests
                </label>
                <p class="control has-icons-left">
                  <input
                    id="guests"
                    v-model="guests"
                    class="input is-medium"
                    type="number"
                    step="1"
                    min="1"
                    max="21"
                    required
                    placeholder="Number of guests">
                  <span class="icon is-small is-left">
                    <i class="mdi mdi-account"/>
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
                  <select v-model="amenities" multiple>
                    <option
                      v-for="amenity in allAmenities"
                      id="capitalize"
                      :key="amenity.id"
                      :value="amenity">{{ amenity.name }}</option>
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
                    v-model="location.title"
                    class="input is-medium"
                    type="text"
                    required
                    placeholder="Location Address (ex. 1600 Amphitheatre Parkway, Mountain View, CA)">
                </div>
              </div>
              <div class="field">
                <input id="files" class="input is-fullwidth" type="file" name="images" @change="readFiles($event.target.files)" multiple>
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
      allAmenities: [],
      address: '',
      location: {
        title: '',
        longtitude: null,
        latitude: null
      },
      price: null,
      description: '',
      title: '',
      guests: 0,
      images: []
    };
  },
  mounted: function() {
    this.$axios.get("/amenities").then(res => {
      this.$data.allAmenities = res.data
    });
  },
  methods: {
    submit() {
      if (!this.$store.getters.isResident) {
        this.$axios.put('/auth/user', {
          is_resident: true
        }).then(() => {
          this.$store.commit('becomeResident')
          console.log(this.$store.getters.isResident)
        })
      }

      this.geocode().then(() => {
        console.log(this.location)

        if (this.location.longtitude && this.location.latitude) {
          this.$axios.post('/listings/', {
            amenities: this.amenities,
            location: this.location,
            price_per_night: this.price,
            guest_amount: this.guests,
            description: this.description,
            title: this.title,
            images: this.images
          }).then(() => {
            this.$toasted.success("Added listing successfully!")
            this.$router.push('/listings')
          }).catch((error) => {
            this.$toasted.error(error.data.message)
          })
        }
      })
      

    },
    readFiles(files) {
      if (files) {
        [].forEach.call(files, this.convertToBase64);
      }
    },
    convertToBase64(file) {
      if ( /\.(jpe?g|png|gif)$/i.test(file.name) ) {
        var reader = new FileReader()
        var self = this
        reader.addEventListener("load", function () {
          var image = new Image()
          image.src = this.result
          self.$data.images.push({ 'image': image.src })
        }, true);

        reader.readAsDataURL(file);
      }
    },
    geocode() {
      return this.$axios
        .get(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(this.location.name)}&key=${this.apiKey}`)
        .then(res => {
          console.log(res.data)
          if (res.data.status === "ZERO_RESULTS") {
            this.$toasted.error("Could not find location's coordinates")
            return
          }
          this.location.longtitude = res.data.results[0].geometry.location.lng.toFixed(6)
          this.location.latitude = res.data.results[0].geometry.location.lat.toFixed(6)
        }).catch(e => {
          console.log(e.data)
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
