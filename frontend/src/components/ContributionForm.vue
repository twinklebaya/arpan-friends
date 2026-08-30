<script setup>
import { ref } from "vue";

import { api } from "../lib/api";
import Button from "./ui/Button.vue";
import Card from "./ui/Card.vue";

const message = ref("");
const contactName = ref("");
const contactEmail = ref("");
const contactPhone = ref("");
const files = ref([]);
const status = ref("idle"); // idle | submitting | success | error
const errorMessage = ref("");

function onFileChange(event) {
  files.value = Array.from(event.target.files || []).slice(0, 5);
}

async function onSubmit() {
  if (!message.value.trim()) return;
  status.value = "submitting";
  errorMessage.value = "";

  const formData = new FormData();
  formData.append("message", message.value.trim());
  if (contactName.value) formData.append("contact_name", contactName.value);
  if (contactEmail.value) formData.append("contact_email", contactEmail.value);
  if (contactPhone.value) formData.append("contact_phone", contactPhone.value);
  for (const file of files.value) formData.append("images", file);

  try {
    await api.submitTip(formData);
    status.value = "success";
    message.value = "";
    contactName.value = "";
    contactEmail.value = "";
    contactPhone.value = "";
    files.value = [];
  } catch (err) {
    status.value = "error";
    errorMessage.value = err.message;
  }
}
</script>

<template>
  <div id="contribute">
    <h2 class="text-lg font-bold text-gray-900">Submit Information</h2>
    <p class="mt-1 text-sm text-gray-500">
      Share anything you know — a sighting, a survivor account, a photo. Every submission is
      reviewed by an admin before it appears publicly, to keep the live feeds accurate.
    </p>

    <Card class="mt-4 p-5">
      <div v-if="status === 'success'" class="rounded-md bg-green-50 p-4 text-sm text-green-800">
        Thank you. Your submission has been received and is <strong>pending admin review</strong>.
        It will not appear publicly until approved.
        <button class="mt-2 block font-medium underline" @click="status = 'idle'">
          Submit another tip
        </button>
      </div>

      <form v-else class="space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="block text-sm font-medium text-gray-700" for="message">
            What do you know? <span class="text-urgent">*</span>
          </label>
          <textarea
            id="message"
            v-model="message"
            required
            rows="4"
            maxlength="5000"
            class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
            placeholder="Describe what you saw, heard, or know — include location and approximate time if possible."
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700" for="images">
            Photos (optional, up to 5)
          </label>
          <input
            id="images"
            type="file"
            accept="image/png,image/jpeg,image/webp,image/gif"
            multiple
            class="mt-1 block w-full text-sm text-gray-600"
            @change="onFileChange"
          />
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <label class="block text-sm font-medium text-gray-700" for="contact_name">Your name</label>
            <input
              id="contact_name"
              v-model="contactName"
              type="text"
              class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700" for="contact_email">Email</label>
            <input
              id="contact_email"
              v-model="contactEmail"
              type="email"
              class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700" for="contact_phone">Phone</label>
            <input
              id="contact_phone"
              v-model="contactPhone"
              type="tel"
              class="mt-1 w-full rounded-md border border-gray-300 p-2 text-sm"
            />
          </div>
        </div>

        <p v-if="status === 'error'" class="text-sm text-urgent">{{ errorMessage }}</p>

        <Button type="submit" variant="urgent" :disabled="status === 'submitting'">
          {{ status === "submitting" ? "Submitting…" : "Submit Information" }}
        </Button>
      </form>
    </Card>
  </div>
</template>
