export type Trip = {
  start: string;
  departure_in: string;
  last_adjusted: string;
  adjusted: boolean;
};

export type Route = {
  route_number: string;
  heading: string;
  trips: Trip[];
};

export type Stop = {
  stop_id: string;
  stop_name: string;
};

export type RouteSummary = {
  stop_metadata: Stop;
  routes: Route[];
};
