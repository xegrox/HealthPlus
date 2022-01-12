const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    '../templates/*.html',
    '../blueprints/**/*.html'
  ],
  theme: {
    extend: {
        fontFamily: {
            sans: ['Inter var', ...defaultTheme.fontFamily.sans]
        },
        colors: {
            primary: '#8c9eff',
            secondary: '#3d5afe',
        },
        transitionProperty: {
            'height': 'height'
          }
    }
  },
  plugins: [],
}
