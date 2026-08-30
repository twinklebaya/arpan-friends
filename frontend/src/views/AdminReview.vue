<script setup>
import { onMounted, ref } from "vue";

import { api, BASE_URL } from "../lib/api";
import Badge from "../components/ui/Badge.vue";
import Button from "../components/ui/Button.vue";
import Card from "../components/ui/Card.vue";

const token = ref(localStorage.getItem("admin_token") || "");
const tokenInput = ref("");
const authError = ref("");

const pendingTips = ref([]);
const pendingSourceUpdates = ref([]);
const persons = ref([]);

const ingestForm = ref({
  raw_text: "",
  source_name: "",
  source_url: "",
  source_type: "other",
  feed_type_hint: "",
});
const ingestResult = ref(null);
const ingestError = ref("");

function saveToken() {
  token.value = tokenInput.value.trim();
  localStorage.setItem("admin_token", token.value);
  refreshAll();
}

function logout() {
  token.value = "";
  localStorage.removeItem("admin_token");
}

async function refreshAll() {
  authError.value = "";
  try {
    pendingTips.value = await api.adminRequest("/api/admin/tips?status=pending", token.value);
    pendingSourceUpdates.value = await api.adminRequest(
      "/api/admin/source-updates?status=pending",
      token.value,
    );
    persons.value = await api.getPersons();
  } catch (err) {
    authError.value = err.message;
  }
}

async function reviewTip(id, action) {
  await api.adminRequest(`/api/admin/tips/${id}`, token.value, {
    method: "PATCH",
    body: JSON.stringify({ action }),
  });
  refreshAll();
}

async function reviewSourceUpdate(id, action) {
  await api.adminRequest(`/api/admin/source-updates/${id}`, token.value, {
    method: "PATCH",
    body: JSON.stringify({ action }),
  });
  refreshAll();
}

async function submitIngest() {
  ingestError.value = "";
  ingestResult.value = null;
  try {
    const payload = { ...ingestForm.value };
    if (!payload.feed_type_hint) delete payload.feed_type_hint;
    if (!payload.source_url) delete payload.source_url;
    ingestResult.value = await api.adminRequest("/api/admin/source-updates", token.value, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    ingestForm.value.raw_text = "";
    refreshAll();
  } catch (err) {
    ingestError.value = err.message;
  }
}

async function setPersonStatus(person, newStatus) {
  await api.adminRequest(`/api/admin/persons/${person.id}`, token.value, {
    method: "PATCH",
    body: JSON.stringify({ status: newStatus }),
  });
  refreshAll();
}

onMounted(() => {
  if (token.value) refreshAll();
});
</script>

<template>
  <div class="mx-auto max-w-4xl space-y-8 px-4 py-8">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-bold text-gray-900">Admin review queue</h1>
      <router-link to="/" class="text-sm text-gray-500 hover:underline">← Back to site</router-link>
    </div>

    <Card v-if="!token" class="p-5">
      <p class="text-sm text-gray-600">Enter the admin token to access the review queue.</p>
      <div class="mt-3 flex gap-2">
        <input
          v-model="tokenInput"
          type="password"
          placeholder="Admin token"
          class="flex-1 rounded-md border border-gray-300 p-2 text-sm"
          @keyup.enter="saveToken"
        />
        <Button @click="saveToken">Enter</Button>
      </div>
    </Card>

    <template v-else>
      <div class="flex justify-end">
        <button class="text-xs text-gray-500 hover:underline" @click="logout">Log out</button>
      </div>
      <p v-if="authError" class="rounded-md bg-red-50 p-3 text-sm text-urgent">{{ authError }}</p>

      <!-- Ingest official/social source updates -->
      <Card class="p-5">
        <h2 class="font-semibold text-gray-900">Ingest a source update</h2>
        <p class="mt-1 text-xs text-gray-500">
          Paste text from an official statement, news article, or a social media post. It runs
          through OpenRouter for classification and lands in the pending queue below — nothing
          publishes until you approve it.
        </p>
        <div class="mt-3 space-y-3">
          <textarea
            v-model="ingestForm.raw_text"
            rows="3"
            placeholder="Paste the excerpt here…"
            class="w-full rounded-md border border-gray-300 p-2 text-sm"
          ></textarea>
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <input
              v-model="ingestForm.source_name"
              placeholder="Source name (e.g. DFAT, @handle)"
              class="rounded-md border border-gray-300 p-2 text-sm"
            />
            <input
              v-model="ingestForm.source_url"
              placeholder="Source URL (optional)"
              class="rounded-md border border-gray-300 p-2 text-sm"
            />
            <select v-model="ingestForm.source_type" class="rounded-md border border-gray-300 p-2 text-sm">
              <option value="official">Official (govt/embassy)</option>
              <option value="news_media">News media</option>
              <option value="social_media">Social media (X, etc.)</option>
              <option value="other">Other</option>
            </select>
          </div>
          <Button :disabled="!ingestForm.raw_text || !ingestForm.source_name" @click="submitIngest">
            Classify &amp; queue for review
          </Button>
          <p v-if="ingestError" class="text-sm text-urgent">{{ ingestError }}</p>
          <pre v-if="ingestResult" class="overflow-x-auto rounded-md bg-gray-50 p-3 text-xs">{{
            JSON.stringify(ingestResult, null, 2)
          }}</pre>
        </div>
      </Card>

      <!-- Pending source updates -->
      <div>
        <h2 class="font-semibold text-gray-900">Pending source updates ({{ pendingSourceUpdates.length }})</h2>
        <div class="mt-3 space-y-3">
          <Card v-for="u in pendingSourceUpdates" :key="u.id" class="p-4">
            <div class="flex items-start justify-between gap-2">
              <div>
                <p class="text-sm font-semibold">{{ u.source_name }}</p>
                <Badge :tone="u.source_type === 'social_media' ? 'warning' : 'neutral'">
                  {{ u.source_type }}
                </Badge>
              </div>
              <div class="flex gap-2">
                <Button variant="outline" @click="reviewSourceUpdate(u.id, 'reject')">Reject</Button>
                <Button @click="reviewSourceUpdate(u.id, 'approve')">Approve</Button>
              </div>
            </div>
            <p class="mt-2 text-sm text-gray-700">{{ u.raw_text }}</p>
            <p v-if="u.ai_summary" class="mt-2 text-sm text-gray-500">
              <strong>AI summary:</strong> {{ u.ai_summary }}
            </p>
            <p v-if="u.ai_status_suggestion" class="mt-1 text-sm text-urgent">
              Suggested status change: {{ u.ai_status_suggestion }} (person id {{ u.ai_person_match_id }})
            </p>
            <p v-if="u.ai_error" class="mt-1 text-xs text-gray-400">{{ u.ai_error }}</p>
          </Card>
          <p v-if="!pendingSourceUpdates.length" class="text-sm text-gray-400">Nothing pending.</p>
        </div>
      </div>

      <!-- Pending tips -->
      <div>
        <h2 class="font-semibold text-gray-900">Pending public tips ({{ pendingTips.length }})</h2>
        <div class="mt-3 space-y-3">
          <Card v-for="t in pendingTips" :key="t.id" class="p-4">
            <div class="flex items-start justify-between gap-2">
              <p class="text-sm font-semibold">{{ t.contact_name || "Anonymous" }}</p>
              <div class="flex gap-2">
                <Button variant="outline" @click="reviewTip(t.id, 'reject')">Reject</Button>
                <Button @click="reviewTip(t.id, 'approve')">Approve</Button>
              </div>
            </div>
            <p class="mt-2 text-sm text-gray-700">{{ t.message }}</p>
            <div v-if="t.image_paths?.length" class="mt-2 flex gap-2">
              <a
                v-for="path in t.image_paths"
                :key="path"
                :href="`${BASE_URL}${path}`"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img :src="`${BASE_URL}${path}`" class="h-16 w-16 rounded object-cover" />
              </a>
            </div>
            <p class="mt-2 text-xs text-gray-400">
              {{ t.contact_email }} {{ t.contact_phone }} — AI notes: {{ t.ai_notes }}
              <span v-if="t.ai_spam_likelihood !== null">
                (spam likelihood: {{ t.ai_spam_likelihood }})
              </span>
            </p>
          </Card>
          <p v-if="!pendingTips.length" class="text-sm text-gray-400">Nothing pending.</p>
        </div>
      </div>

      <!-- Manual person status corrections -->
      <div>
        <h2 class="font-semibold text-gray-900">Person records</h2>
        <div class="mt-3 overflow-x-auto rounded-lg border border-gray-200">
          <table class="min-w-full divide-y divide-gray-200 text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-2 text-left">Name</th>
                <th class="px-3 py-2 text-left">Status</th>
                <th class="px-3 py-2 text-left">Change</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 bg-white">
              <tr v-for="p in persons" :key="p.id">
                <td class="px-3 py-2">{{ p.name }}</td>
                <td class="px-3 py-2">
                  <Badge :tone="p.status === 'deceased' ? 'urgent' : 'warning'">{{ p.status }}</Badge>
                </td>
                <td class="px-3 py-2">
                  <select
                    class="rounded-md border border-gray-300 p-1 text-xs"
                    :value="p.status"
                    @change="setPersonStatus(p, $event.target.value)"
                  >
                    <option value="missing">missing</option>
                    <option value="deceased">deceased</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p class="mt-2 text-xs text-gray-400">
          Manual override — use only when you have independent verified confirmation. Prefer the
          source-update review flow above so there is an audit trail.
        </p>
      </div>
    </template>
  </div>
</template>
