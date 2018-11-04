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
            <figure class="image is-16by9">
              <img :src="listing.images[0].image">
            </figure>
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-content has-text-centered">
                <p class="title is-4">{{ listing.title }}</p>
                <p class="subtitle is-6">{{ listing.location.title }} &bull; ${{ listing.price_per_night }}/night</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </transition-group >
    <nuxt-link
      v-if="$store.getters.isResident"
      class="btn-circle btn-lg has-background-dark tooltip"
      data-tooltip="Add Listing"
      to="/listings/add">
      <i class="mdi mdi-plus"/>
    </nuxt-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      listings: []
    };
  },
  mounted() {
    let url = new URL(`${this.$axios.defaults.baseURL}/listings`)
    if (this.$route.query.search) {
      url.searchParams.append('search', this.$route.query.search);
    }
    if (this.$route.query.free_from) {
      url.searchParams.append('free_from', this.$route.query.free_from);
    }
    if (this.$route.query.free_to) {
      url.searchParams.append('free_to', this.$route.query.free_to);
    }
    return this.$axios.get(url).then(res => {
      this.listings = res.data;
    });
  }
};
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
  -webkit-filter: drop-shadow(8px 8px 10px black);
  -moz-filter: drop-shadow(8px 8px 10px black);
  filter: drop-shadow(8px 8px 10px black);
  transition: all 0.5s ease;
}
.list-item {
  display: inline-block;
  margin-right: 10px;
}
.list-enter-active,
.list-leave-active {
  transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}

.btn-circle.btn-lg {
    position: fixed;
    z-index: 1;
    right: 0.5em;
    bottom: 2em;
    border: none;
    border-radius: 50%;
    height: 60px;
    width: 60px;
    padding: 10px 16px;
    font-size: 20px;
    line-height: 1.33;
}

.btn-circle i {
    font-size: 28px;
    color: white;
}

.btn-circle i:hover {
    color: gold;
}

.tooltip::after{
  padding: 0rem;
  box-shadow: none;
  -webkit-box-shadow: none;
  border-radius: 0px;
}
</style>
