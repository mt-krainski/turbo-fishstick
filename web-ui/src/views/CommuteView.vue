<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';

const routeSummary = ref<any>();
const routeRefreshInterval = 15000;
const loading = ref<boolean>(false);

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

function reformatRoutes(
  routes: RouteSummary
): { type?: string; title?: string; value?: number }[] {
  const reformattedRoutes: any[] = [];
  let id = 0;
  reformattedRoutes.push({
    title: `${routes.stop_metadata.stop_name}`,
  });
  for (const route of routes.routes) {
    reformattedRoutes.push({
      type: 'subheader',
      title: `${route.route_number} - ${route.heading}`,
    });
    for (const trip of route.trips) {
      reformattedRoutes.push({
        title: `${trip.start} in ${trip.departure_in} min. ${
          trip.adjusted ? '*' : ''
        }`,
        value: id++,
      });
    }
    reformattedRoutes.push({ type: 'divider' });
  }
  // Remove the last divider
  reformattedRoutes.pop();
  return reformattedRoutes;
}

async function refreshRoute() {
  loading.value = true;
  const routeSummaryResponse = await axios.get(
    'http://localhost:8000/commute/route_summary',
    {
      params: {
        trip_variant: 'home',
      },
    }
  );
  routeSummary.value = reformatRoutes(
    routeSummaryResponse.data as RouteSummary
  );
  loading.value = false;
}

setInterval(refreshRoute, routeRefreshInterval);

onMounted(() => {
  refreshRoute();
});
</script>

<template>
  <div class="d-flex align-center flex-column">
    <v-card class="mx-auto mt-12" width="400" variant="tonal">
      <p class="text-center pa-3">
        <v-icon icon="mdi-bus" />
      </p>
      <div v-if="loading">
        <p class="text-center pa-10">
          <v-progress-circular
            indeterminate
            model-value="20"
            :size="79"
            :width="10"
          ></v-progress-circular>
        </p>
      </div>
      <div v-else>
        <v-list :items="routeSummary"></v-list>
      </div>
    </v-card>
  </div>
</template>

<style></style>
