/* eslint-disable */

// ─────────────────────────────────────────────────────────────
//  Flight‑Booking Web Form client script
//  Pre‑fills a new Airplane Ticket from ?flight=<name> param
// ─────────────────────────────────────────────────────────────
frappe.web_form.before_load = () => {
  // Grab flight parameter from URL
  const params  = new URLSearchParams(window.location.search);
  const flight  = params.get("flight");

  if (!flight) return;                       // nothing to pre‑fill

  // Fill the hidden/readonly Flight link immediately
  frappe.web_form.set_value("flight", flight);

  // Fetch flight details in one call
  frappe.call({
    method: "frappe.client.get_value",
    args: {
      doctype: "Airplane Flight",
      filters: { name: flight },
      fieldname: [
        "source_airport",
        "destination_airport",
        "date_of_departure",
        "time_of_departure",
        "duration",
        "flight_price"
      ]
    },
    callback: ({ message }) => {
      if (!message) return;

      frappe.web_form.set_value("source_airport",       message.source_airport);
      frappe.web_form.set_value("destination_airport",  message.destination_airport);
      frappe.web_form.set_value("departure_date",       message.date_of_departure);
      frappe.web_form.set_value("departure_time",       message.time_of_departure);
      frappe.web_form.set_value("duration_of_flight",   message.duration);
      frappe.web_form.set_value("flight_price",         message.flight_price);
    }
  });
};
