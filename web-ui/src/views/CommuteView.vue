<script setup lang="ts">
import { onMounted, ref } from 'vue';
import axios from 'axios';

import type { RouteSummary } from '../types/commute-types';

const routeSummary = ref<any>();
const routeRefreshInterval = 15000;
const firstTimeLoaded = ref<boolean>(false);

// TODO: make this an env variable
const serverPath = '';

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
  const routeSummaryResponse = await axios.get(
    `${serverPath}/api/commute/route_summary`,
    {
      params: {
        trip_variant: 'home',
      },
    }
  );
  routeSummary.value = reformatRoutes(
    routeSummaryResponse.data as RouteSummary
  );
  firstTimeLoaded.value = true;
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
      <div v-if="!firstTimeLoaded">
        <p class="text-center pa-10">
          <v-progress-circular
            indeterminate
            :size="80"
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
