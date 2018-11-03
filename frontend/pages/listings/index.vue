<template>
  <div class="container">
    <transition-group 
      class="columns is-multiline"
      name="list"
      tag="section">
      <div
        v-for="listing in listings"
        :key="listing.id"
        :id="`listing-${listing.id}`"
        class="column is-4 listing">

        <div 
          class="card"
          @click="$router.push(`/listings/${listing.id}`)">
          <div class="card-image">
            <figure class="image">
              <img src="https://media.equityapartments.com/images/c_crop,x_0,y_0,w_1920,h_1080/c_fill,w_1920,h_1080/q_80/4011-1/moda-apartments-exterior.jpg">
            </figure>
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-content has-text-centered">
                <p class="title is-4">{{ listing.title }}</p>
                <p class="subtitle is-6">{{ listing.location.name }} 	&bull; ${{ listing.price_per_night }}/night</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition-group >
  </div>
</template>

<script>
export default {
  data() {
    return {
      listings: []
    }
  },
  mounted() {
    let url = this.$route.query.search ? `/listings?search=${this.$route.query.search}` : '/listings'
    return this.$axios.get(url)
    .then((res) => {
      this.listings = res.data
    })
  }

}
</script>

<style>
  .container {
    margin-top: 2%;
  }
  .card {
    border: 15px solid white;
    border-radius: 5px;
    cursor: pointer;
  }
  .card:hover {
    -webkit-filter:drop-shadow(8px 8px 10px black);
    -moz-filter:drop-shadow(8px 8px 10px black);
    filter:drop-shadow(8px 8px 10px black);
    transition: all 0.5s ease;
  }
  .list-item {
    display: inline-block;
    margin-right: 10px;
  }
  .list-enter-active, .list-leave-active {
    transition: all 1s;
  }
  .list-enter, .list-leave-to {
    opacity: 0;
    transform: translateY(30px);
  }
</style>
