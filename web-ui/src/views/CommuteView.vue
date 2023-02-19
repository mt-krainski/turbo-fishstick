<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';

const routeSummary = ref<RouteSummary>();
const routeRefreshInterval = 15000;

type Trip = {
  start: string;
  departure_in: string;
  last_adjusted: string;
  adjusted: boolean;
};

type Route = {
  route_number: string;
  heading: string;
  trips: Trip[];
};

type Stop = {
  stop_id: string;
  stop_name: string;
};

type RouteSummary = {
  stop_metadata: Stop;
  routes: Route[];
};

async function refreshRoute() {
  const routeSummaryResponse = await axios.get(
    'http://localhost:8000/commute/route_summary',
    {
      params: {
        trip_variant: 'home',
      },
    }
  );
  routeSummary.value = routeSummaryResponse.data as RouteSummary;
}

setInterval(refreshRoute, routeRefreshInterval);

onMounted(() => {
  refreshRoute();
});
</script>

<template>
  <div class="about">
    <h1 v-if="routeSummary">
      ({{ routeSummary.stop_metadata.stop_id }})
      {{ routeSummary.stop_metadata.stop_name }}
      <div v-for="route in routeSummary.routes">
        ({{ route.route_number }}) {{ route.heading }}
        <li v-for="trip in route.trips">
          {{ trip.start }} in {{ trip.departure_in }} min.
          {{ trip.adjusted ? '*' : '' }}
        </li>
      </div>
    </h1>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
