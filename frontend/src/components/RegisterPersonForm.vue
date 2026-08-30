<script setup>
import { ref } from "vue";

import { api } from "../lib/api";
import Button from "./ui/Button.vue";
import Card from "./ui/Card.vue";

const form = ref({
  name: "",
  age: "",
  status: "missing",
  last_seen_location: "",
  found_location: "",
  physical_markers: "",
  submitted_by_name: "",
  submitted_by_email: "",
  submitted_by_phone: "",
});
const status = ref("idle"); // idle | submitting | success | error
const errorMessage = ref("");

async function onSubmit() {
  if (!form.value.name.trim()) return;
  status.value = "submitting";
  errorMessage.value = "";

  const payload = {
    name: form.value.name.trim(),
    age: form.value.age ? Number(form.value.age) : null,
    status: form.value.status,
    last_seen_location: form.value.last_seen_location,
    found_location: form.value.status === "deceased" ? form.value.found_location : null,
    physical_markers: form.value.physical_markers,
    submitted_by_name: form.value.submitted_by_name || null,
    submitted_by_email: form.value.submitted_by_email || null,
    submitted_by_phone: form.value.submitted_by_phone || null,
  };

  try {
    await api.submitPerson(payload);
    status.value = "success";
    form.value = {
      name: "",
      age: "",
      status: "missing",
      last_seen_location: "",
      found_location: "",
      physical_markers: "",
      submitted_by_name: "",
      submitted_by_email: "",
      submitted_by_phone: "",
    };
  } catch (err) {
    status.value = "error";
    errorMessage.value = err.message;
  }
}
</script>

<template>
  <section id="register-person" class="mx-auto max-w-3xl px-4 py-8">
    <h2 class="text-lg font-bold text-gray-900">Register a Missing or Deceased Loved One</h2>
    <p class="mt-1 text-sm text-gray-500">
      This hub is open to families and friends of anyone affected by the Nepal-Tibet floods, of
      any nationality — not only the Kailash Journeys group. Entries are reviewed by an admin
      before appearing in the public tables above, to keep the registry accurate.
    </p>

    <Card class="mt-4 p-5">
      <div v-if="status === 'success'" class="rounded-md bg-green-50 p-4 text-sm text-green-800">
        Thank you. This entry has been received and is <strong>pending admin review</strong>. It
        will appear in the tables above once approved.
        <button class="mt-2 block font-medium underline" @click="status = 'idle'">
          Register another person
        </button>
      </div>

      <form v-else class="space-y-4" @submit.prevent="onSubmit">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700" for="p-name">
              Full name <span class="text-urgent">*</span>
            </label>
            <input
              id="p-name"
              v-model="form.name"
              required
              type="text"
              class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700" for="p-age">Age</label>
            <input
              id="p-age"
              v-model="form.age"
              type="number"
              min="0"
              max="130"
              class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700" for="p-status">Status</label>
          <select
            id="p-status"
            v-model="form.status"
            class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
          >
            <option value="missing">Missing</option>
            <option value="deceased">Deceased (officially confirmed)</option>
          </select>
          <p v-if="form.status === 'deceased'" class="mt-1 text-xs text-urgent">
            Only submit as deceased if this has been officially confirmed (e.g. by authorities or
            a hospital/mortuary) — an admin will verify before this is published.
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700" for="p-last-seen">
            Last seen location / circumstances
          </label>
          <textarea
            id="p-last-seen"
            v-model="form.last_seen_location"
            rows="2"
            class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
          ></textarea>
        </div>

        <div v-if="form.status === 'deceased'">
          <label class="block text-sm font-medium text-gray-700" for="p-found">
            Location found
          </label>
          <input
            id="p-found"
            v-model="form.found_location"
            type="text"
            class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700" for="p-markers">
            Distinct physical markers (for identification)
          </label>
          <textarea
            id="p-markers"
            v-model="form.physical_markers"
            rows="2"
            class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
          ></textarea>
        </div>

        <p class="text-xs text-gray-500">
          Your contact info below is for admin follow-up only — it is never shown publicly.
        </p>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <input
            v-model="form.submitted_by_name"
            type="text"
            placeholder="Your name"
            class="rounded-md border border-gray-300 p-2 text-sm"
          />
          <input
            v-model="form.submitted_by_email"
            type="email"
            placeholder="Your email"
            class="rounded-md border border-gray-300 p-2 text-sm"
          />
          <input
            v-model="form.submitted_by_phone"
            type="tel"
            placeholder="Your phone"
            class="rounded-md border border-gray-300 p-2 text-sm"
          />
        </div>

        <p v-if="status === 'error'" class="text-sm text-urgent">{{ errorMessage }}</p>

        <Button type="submit" :disabled="status === 'submitting'">
          {{ status === "submitting" ? "Submitting…" : "Register" }}
        </Button>
      </form>
    </Card>
  </section>
</template>
