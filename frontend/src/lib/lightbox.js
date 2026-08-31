import { reactive } from "vue";

export const lightboxState = reactive({ url: null, alt: "" });

export function openLightbox(url, alt = "") {
  lightboxState.url = url;
  lightboxState.alt = alt;
}

export function closeLightbox() {
  lightboxState.url = null;
}
