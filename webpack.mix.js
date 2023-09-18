const mix = require('laravel-mix');
const sass = require('sass');

mix.sass('static/styles.scss', 'output.css')
   .options({
      processCssUrls: false,
      postCss: [require('tailwindcss')('./tailwind.config.js')],
   })
   .setPublicPath('static');