<template>
  <section class="column hero is-danger is-bold is-10 is-offset-1">
    <div class="hero-body">
      <div class="box">
        <h1 class="title has-text-centered has-text-dark">
          {{ title }}
        </h1>
        <no-ssr>
          <vueper-slides 
            fade
            v-if="slides.length > 0"
            slide-content-outside="top"
            slide-content-outside-class="max-widthed"
            :touchable="false"
            :slide-ratio="0.3"
            ref="vueperSlides">
            <vueper-slide
              aria-hidden="false"
              :class="{ 'vueperslide--active': slide.id === 0 }"
              v-for="slide in slides"
              :key="slide.id"
              :image="slide.image_url"/>
          </vueper-slides>
          <img
            v-else
            :src="slides[0]"/>
        </no-ssr>
        
        <hr class="break">
        <div class="columns">
          <section class="column is-8 is-medium has-text-justified">
            {{ description }}
            <hr>
            <iframe
              width="600"
              height="450"
              frameborder="0" style="border:0"
              :src="`https://www.google.com/maps/embed/v1/place?key=${apiKey}
                &q=${location.title || 'Sofia'}`" 
              allowfullscreen>
            </iframe>
          </section>
          <div class="column is-4 is-medium">
            <div class="guest has-text-weight-bold is-large">
              <i class="mdi mdi-account"></i>
              <span>Max. Guests: {{ guests }}</span>
            </div>
            <br>
            <div class="content has-text-weight-bold">
              <i class="mdi mdi-airplay"></i>
              Amenities:
              <ul>
                <li v-for="amenity in amenities" :key="amenity.id"> {{ amenity.name }}</li>
              </ul>
            </div>
            
            <b-field class="is-fullwidth">
              <b-datepicker
                v-model="checkInDate"
                :min-date="new Date(today.getFullYear(), today.getMonth(), today.getDate())"
                name="checkInDate"
                :unselectable-dates="bookedDates"
                placeholder="Check in"
                @input="nearestFutureAvailableDate(checkInDate); setMinCheckOutDate(checkInDate)"
                icon="calendar-today"
                required/>
              <b-datepicker
                v-model="checkOutDate"
                :min-date="minCheckOutDate"
                :max-date="maxCheckOutDate"
                :unselectable-dates="bookedDates"
                name="checkOutDate"
                placeholder="Check out"
                icon="calendar-today" 
                required/>
            </b-field>
              <button class="button is-fullwidth is-dark" @click="book">Book</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { VueperSlides, VueperSlide } from 'vueperslides'
import 'vueperslides/dist/vueperslides.min.css'

export default {
  components: { VueperSlides, VueperSlide },
  created() {
    this.$axios.get(`/listings/${this.$route.params.id}/`)
      .then(res => {
        this.slides = res.data.images,
        this.title = res.data.title,
        this.description = res.data.description
        this.price = res.data.price_per_night
        this.location = res.data.location
        this.amenities = res.data.amenities
        this.bookings = res.data.bookings
        this.guests = res.data.guest_amount

        this.bookings.forEach(booking => {
          this.bookedDates.push(...this.getDates(new Date(booking.check_in), new Date(booking.check_out)))
        });
      })
  },
  data() {
    return {
      slides: [],
      title: '',
      description: '',
      price: '',
      amenities: [],
      location: {
        title: '',
        longitude: 0,
        latitude: 0
      },
      guests: 0,
      bookings: [],
      today: new Date(),
      bookedDates: [],
      checkInDate: null,
      checkOutDate: null,
      minCheckOutDate: new Date(),
      maxCheckOutDate: new Date(86400000000000),
      apiKey: process.env.GEOCODE_API_KEY
    }
  },
  methods: {
    getDates: function(startDate, endDate) {
      var dates = [],
          currentDate = startDate,
          addDays = function(days) {
            var date = new Date(this.valueOf());
            date.setDate(date.getDate() + days);
            return date;
          };
      while (currentDate <= endDate) {
        dates.push(currentDate);
        currentDate = addDays.call(currentDate, 1);
      }
      return dates;
    },
    nearestFutureAvailableDate: function(date) {
      var now = new Date(date);
      var closest = new Date(8640000000000)

      this.bookedDates.forEach(function(d) {
        var date = new Date(d);
        if (date >= now && date < closest) {
            closest = d;
        }
      });

      this.maxCheckOutDate = closest
    },
    book() {
      if (!this.$store.getters.isLoggedIn) {
        this.$router.push('/auth/login')
      }

      this.$axios.post(`/listings/${this.$route.params.id}/bookings/`, {
        check_in: this.$moment(this.checkInDate).format('YYYY-MM-DD'),
        check_out: this.$moment(this.checkOutDate).format('YYYY-MM-DD')
      }).then(() => {
        this.$toasted.success("Successfully made booking for the requested dates.")
        this.$router.push('/bookings')
      }).catch(e => {
        this.$toasted.error(JSON.stringify(e.response.data))
      })
    },
    setMinCheckOutDate(checkInDate) {
      var result = new Date(checkInDate)
      result.setDate(result.getDate() + 1)
      this.minCheckOutDate = result
    }
  },
  transition: "bounce"
}
</script>

<style>
  .vueperslide__content-wrapper--outside-top {
    transition: 0.2s ease-in-out;
    opacity: 1;
    transform: scale(1);
  }

  .vueperslides--animated .vueperslide__content-wrapper--outside-top {
    transition: 0.15s ease-in-out;
    opacity: 0;
    transform: scale(0);
  }
</style>
