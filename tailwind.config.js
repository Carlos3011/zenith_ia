/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/**/*.html',  // Buscar clases en las plantillas Django
    './core/static/js/**/*.js',    // Si usas JS con Tailwind
  ],
  theme: {
    extend: {
      colors: {
        'calm-blue': '#E3F2FD',
        'soothing-green': '#E8F5E9',
        'warm-purple': '#F3E5F5',
        'primary': '#5B21B6',
        'secondary': '#4F46E5',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
