/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // HTML 템플릿 파일
    "./static/**/*.js", // JS 파일 (있다면)
  ],
  theme: {
    extend: {
      colors: {
        primary: "#DE4773", // 예시: primary 색상
        primary_dark: "#C93561", // 예시: secondary 색상
        search_bg: "#F3F4F6", // 예시: 검색창 배경색
        search_text: "#9AA0AE", // 예시: 검색창 텍스트 색상
        background: "#FCFCFD", // 예시: 배경색
      },
    },
  },
  plugins: [],
};
