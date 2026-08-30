/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        urgent: {
          DEFAULT: "#b91c1c",
          light: "#fee2e2",
        },
      },
    },
  },
  plugins: [],
};
