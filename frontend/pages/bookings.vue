<template>
  <div class="container">
    <div v-for="booking in bookings" :key="booking.id" class="card">
      <header class="card-header">
        <p class="card-header-title">
          {{ booking.listing.title }}
        </p>
        <a href="#" class="card-header-icon" aria-label="more options">
          <span class="icon">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </a>
      </header>
      <div class="card-content">
        <div class="media">
          <div class="media-left">
            <figure class="image is-128x128">
              <img :src="booking.listing.images[0].image_url">
            </figure>
          </div>
          <div class="media-right">
            <p>
              Booked from <span class="is-italic has-text-weight-bold">{{ $moment(booking.check_in).format('DD MMM YYYY') }} to {{ $moment(booking.check_out).format('DD MMM YYYY') }}</span>. A place for {{ booking.listing.guest_amount }}.
            </p> 
            <p>
              Total price: ${{ ($moment(booking.check_out).diff($moment(booking.check_in), 'days')) * booking.listing.price_per_night }}
            </p>
          </div>
        </div>
      <footer class="card-footer">
        <nuxt-link
          :to="`/listings/${booking.listing.id}`"
          class="card-footer-item has-text-white has-background-dark">
          View Listing
        </nuxt-link>
      </footer>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  middleware: [
    'auth'
  ],
  data() {
    return {
      bookings: []
    };
  },
  mounted() {
    this.$axios.get(`/bookings/user/`).then(res => {
      this.bookings = res.data;
    });
  }
};
</script>

<style>
.card {
  margin: 20px;
}
</style>
