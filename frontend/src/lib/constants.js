// Precise last-known coordinate for the group, reconstructed by the family:
// Apple location data from Mr. Suresh's phone (part of the same group)
// recorded 28.26584 N, 85.37584 E at 7:51am Nepal time on Aug 26, 2026; his
// phone's connection was lost at 8:28am. This is far more precise than any
// published regional marker (e.g. Wikipedia's 28.3 N, 85.5 E for the whole
// Gyirong/Rasuwa flood zone) since it comes from an actual device location
// fix for someone travelling with the group.
export const LAST_KNOWN_LOCATION = {
  lat: 28.26584,
  lng: 85.37584,
  label: "Last recorded phone location, Mr. Suresh (group member), near Timure / Rasuwagadhi border, Nepal",
  note: "Family-sourced: Apple location data, 7:51am Nepal time, Aug 26 2026. His phone lost connection at 8:28am. Not an official/surveyed coordinate.",
};

export const MAP_DEFAULT_ZOOM = 10;

// Town-level approximate coordinates -- these are NOT precise street
// addresses (none were found in public reporting), just honest
// town-center pins so the map is still useful for general orientation.
export const RESOURCE_PINS = [
  {
    lat: 28.1667,
    lng: 85.3333,
    label: "Rasuwa District Hospital",
    category: "hospital",
    note: "Dhunche (Rasuwa district HQ) -- approximate town-center pin, not a surveyed address.",
  },
  {
    lat: 27.9667,
    lng: 85.05,
    label: "Trishuli District Hospital",
    category: "hospital",
    note: "Trishuli Bazaar, Nuwakot -- approximate town-center pin, not a surveyed address.",
  },
  {
    lat: 27.7172,
    lng: 85.324,
    label: "Kathmandu hospitals (multiple)",
    category: "hospital",
    note: "General Kathmandu city pin -- flood casualties were distributed across several city hospitals.",
  },
  {
    lat: 27.9167,
    lng: 85.1667,
    label: "Maithili Army Camp (survivor shelter)",
    category: "shelter",
    note: "Nuwakot -- Nepal Army camp where evacuated survivors were sheltered in tents. Approximate town-level pin.",
  },
];
