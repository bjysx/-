export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef6ff",
          100: "#d9ebff",
          500: "#2563eb",
          600: "#1d4ed8",
          700: "#1e40af"
        }
      },
      boxShadow: {
        panel: "0 16px 40px rgba(15, 23, 42, 0.12)"
      },
      backgroundImage: {
        hero: "radial-gradient(circle at top left, rgba(37,99,235,0.18), transparent 40%), linear-gradient(135deg, #0f172a, #1d4ed8)"
      }
    }
  },
  plugins: []
}
