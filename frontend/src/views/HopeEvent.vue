<script setup>
import { computed, onMounted, ref } from "vue";

import { api } from "../lib/api";
import Button from "../components/ui/Button.vue";
import SocialShare from "../components/SocialShare.vue";

const HOPE_URL = "https://findingarpan.vercel.app/hope";
const HOPE_SHARE_TEXT = 'Join the Global "Rasuwa Hope and Awareness" event, Sunday, September 6 at 5 PM Pacific.';

const loveCount = ref(0);
const hasLoved = ref(false);
const loving = ref(false);

const comments = ref([]);
const commentsLoading = ref(true);
const commentName = ref("");
const commentMessage = ref("");
const commentSubmitting = ref(false);
const commentError = ref("");

const COMMENTS_PER_PAGE = 10;
const commentPage = ref(1);
const totalCommentPages = computed(() =>
  Math.max(1, Math.ceil(comments.value.length / COMMENTS_PER_PAGE)),
);
const pagedComments = computed(() => {
  const start = (commentPage.value - 1) * COMMENTS_PER_PAGE;
  return comments.value.slice(start, start + COMMENTS_PER_PAGE);
});

onMounted(async () => {
  hasLoved.value = localStorage.getItem("hope-event-loved") === "1";
  try {
    const stats = await api.getHopeStats();
    loveCount.value = stats.love_count;
  } catch {
    // non-critical -- leave the count at 0 if the API is unreachable
  }
  await loadComments();
});

async function loadComments() {
  commentsLoading.value = true;
  try {
    comments.value = await api.getHopeComments();
  } catch {
    comments.value = [];
  } finally {
    commentsLoading.value = false;
  }
}

async function sendLove() {
  if (hasLoved.value || loving.value) return;
  loving.value = true;
  try {
    const stats = await api.loveHopeEvent();
    loveCount.value = stats.love_count;
    hasLoved.value = true;
    localStorage.setItem("hope-event-loved", "1");
  } catch {
    // ignore -- button just stays clickable if the request failed
  } finally {
    loving.value = false;
  }
}

function formatTime(iso) {
  const hasTimezone = /Z$|[+-]\d\d:\d\d$/.test(iso);
  const utcIso = hasTimezone ? iso : `${iso}Z`;
  return new Date(utcIso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

async function submitComment() {
  const message = commentMessage.value.trim();
  if (!message) return;
  commentSubmitting.value = true;
  commentError.value = "";
  try {
    await api.submitHopeComment({
      author_name: commentName.value.trim() || null,
      message,
    });
    commentMessage.value = "";
    commentPage.value = 1;
    await loadComments();
  } catch {
    commentError.value = "Couldn't post your comment. Please try again.";
  } finally {
    commentSubmitting.value = false;
  }
}
</script>

<template>
  <div class="bg-white">
    <section class="bg-gray-900 text-white">
      <div class="mx-auto max-w-7xl px-4 py-10 sm:py-14">
        <router-link to="/" class="text-sm text-gray-400 hover:text-white hover:underline">
          &larr; Back to the search hub
        </router-link>
        <p class="mt-4 text-sm font-semibold uppercase tracking-wide text-red-400">
          Virtual and In-person
        </p>
        <h1 class="mt-2 text-2xl font-bold leading-tight sm:text-4xl">
          Global Event: Rasuwa Hope and Awareness
        </h1>
        <dl class="mt-6 grid grid-cols-1 gap-6 text-sm sm:grid-cols-3">
          <div>
            <dt class="font-semibold uppercase tracking-wide text-gray-400">When</dt>
            <dd class="mt-1 space-y-1 text-gray-200">
              <p>Sun, Sept 6 &middot; 5:00 PM Pacific (USA)</p>
              <p>Sun, Sept 6 &middot; 8:00 PM Eastern (Canada)</p>
              <p>Mon, Sept 7 &middot; 8:00 AM Malaysia (MYT)</p>
              <p>Mon, Sept 7 &middot; 10:00 AM Australia Eastern (AEST)</p>
            </dd>
          </div>
          <div>
            <dt class="font-semibold uppercase tracking-wide text-gray-400">Where</dt>
            <dd class="mt-1 text-gray-200">TBD</dd>
          </div>
          <div>
            <dt class="font-semibold uppercase tracking-wide text-gray-400">Hosted from</dt>
            <dd class="mt-1 text-gray-200">San Francisco Bay Area</dd>
          </div>
        </dl>
        <div class="mt-6 rounded-lg border border-gray-700 bg-gray-800 p-4 text-sm text-gray-300">
          <span class="font-semibold text-white">Meeting link:</span>
          will be posted here shortly &mdash; check back closer to the event. No registration is
          required to attend.
        </div>

        <div class="mt-6 flex flex-wrap items-center gap-4">
          <button
            type="button"
            :disabled="hasLoved || loving"
            @click="sendLove"
            class="flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold transition"
            :class="
              hasLoved
                ? 'border-urgent bg-urgent-light text-urgent'
                : 'border-gray-600 bg-gray-800 text-gray-200 hover:border-urgent hover:text-urgent'
            "
          >
            <span aria-hidden="true">🙏</span>
            {{ hasLoved ? "You sent hope & prayers" : "Send hope & prayers" }}
          </button>
          <span class="text-sm text-gray-400">{{ loveCount }} people have sent hope & prayers</span>
          <SocialShare inline :url="HOPE_URL" :text="HOPE_SHARE_TEXT" />
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-4 py-10">
      <div class="grid grid-cols-1 gap-10 lg:grid-cols-3">
        <div class="lg:col-span-2">
          <blockquote class="border-l-4 border-urgent pl-4 italic text-gray-700">
            <p>Sisters are missing their brothers.</p>
            <p>Children are missing their mothers.</p>
            <p>Wives are missing their husbands.</p>
            <p class="mt-3 not-italic font-semibold text-gray-900">
              The pain cannot be explained, it can only be felt.
            </p>
          </blockquote>

          <p class="mt-8 text-gray-700">
            The Rasuwa floods have impacted people all over the world, with nearly 5,000 people
            still missing. Many of those impacted were pilgrims to Mount Kailash from over 20
            different countries.
          </p>
          <p class="mt-4 text-gray-700">
            Now as hours have rolled into days and days into weeks, a lot of families all over the
            world are distressed by the lack of information about the whereabouts and safety of
            their loved ones. No one is able to share information that will help reduce the pain
            of those who are waiting for them.
          </p>
          <p class="mt-4 text-gray-700">
            This event is to give hope to such families &mdash; whether they are in the USA,
            Australia, Canada, Malaysia, and many other countries &mdash; that there is still a
            way they can be reunited with their families. We are bringing together those who are
            safe to give an account of their own experience and clarify the circumstances through
            which they have managed to come back to their lives, so that it can provide clarity to
            others who have many more questions than answers.
          </p>
        </div>

        <div class="lg:col-span-1">
          <div class="rounded-lg border border-gray-200 bg-gray-50 p-5 lg:sticky lg:top-6">
            <h2 class="text-lg font-bold uppercase tracking-wide text-gray-900">Messages of Hope</h2>

            <form class="mt-4 space-y-3" @submit.prevent="submitComment">
              <input
                v-model="commentName"
                type="text"
                maxlength="100"
                placeholder="Your name (optional)"
                class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-urgent focus:outline-none"
              />
              <textarea
                v-model="commentMessage"
                required
                maxlength="2000"
                rows="3"
                placeholder="Share a message of support or hope..."
                class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-urgent focus:outline-none"
              ></textarea>
              <div class="flex items-center gap-3">
                <Button type="submit" variant="urgent" :disabled="commentSubmitting">
                  {{ commentSubmitting ? "Posting..." : "Post message" }}
                </Button>
                <p v-if="commentError" class="text-sm text-red-600">{{ commentError }}</p>
              </div>
            </form>

            <div class="mt-6 space-y-4">
              <p v-if="commentsLoading" class="text-sm text-gray-400">Loading comments...</p>
              <p v-else-if="!comments.length" class="text-sm text-gray-400">
                No comments yet. Be the first to share a message.
              </p>
              <div
                v-for="c in pagedComments"
                :key="c.id"
                class="rounded-lg border border-gray-200 bg-white p-4"
              >
                <div class="flex items-center justify-between gap-2">
                  <p class="text-sm font-semibold text-gray-900">
                    {{ c.author_name || "Anonymous" }}
                  </p>
                  <p class="text-xs text-gray-400">{{ formatTime(c.created_at) }}</p>
                </div>
                <p class="mt-1 whitespace-pre-wrap text-sm text-gray-700">{{ c.message }}</p>
              </div>
            </div>

            <div
              v-if="comments.length > COMMENTS_PER_PAGE"
              class="mt-4 flex items-center justify-between text-sm"
            >
              <button
                type="button"
                :disabled="commentPage === 1"
                @click="commentPage--"
                class="font-medium text-gray-600 hover:text-urgent disabled:cursor-not-allowed disabled:text-gray-300"
              >
                &larr; Previous
              </button>
              <span class="text-gray-500">Page {{ commentPage }} of {{ totalCommentPages }}</span>
              <button
                type="button"
                :disabled="commentPage === totalCommentPages"
                @click="commentPage++"
                class="font-medium text-gray-600 hover:text-urgent disabled:cursor-not-allowed disabled:text-gray-300"
              >
                Next &rarr;
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
