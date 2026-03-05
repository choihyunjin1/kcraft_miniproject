/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // HTML 템플릿 파일
    "./static/**/*.js", // JS 파일 (있다면)
  ],
  theme: {
    extend: {
      colors: {
        primary: "#DE4773",
        primary_dark: "#C93561",
        search_bg: "#F3F4F6",
        search_text: "#9AA0AE",
        background: "#FCFCFD",
        card_bg: "#FFFFFF",
        card_border: "E5E7EA",
        plain_text: "#000000",
      },
    },
  },
  plugins: [],
};
