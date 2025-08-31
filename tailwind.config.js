/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5ff6f7',
          100: '#e0e2e4',
          200: '#c2c6ca',
          300: '#a3aab0',
          400: '#707980',
          500: '#353b41', // MAIN COLOUR!!!
          600: '#2f343a',
          700: '#282c32',
          800: '#212429',
          900: '#1a1c21',
        },
      },
    },
  },
  plugins: [],
}

