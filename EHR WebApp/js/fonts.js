// Web Font Loader.
// @see https://github.com/typekit/webfontloader
// eslint-disable-next-line no-undef
WebFontConfig = {
  custom: {
    families: ['Verlag', 'prometo'],
    urls: ['/sites/all/themes/hde/fonts/fonts.css', 'https://use.typekit.net/vzq7qoi.css']
  }
};

(function (d) {
  const wf = d.createElement('script');
  const s = d.scripts[0];
  wf.src = 'https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js';
  wf.async = true;
  s.parentNode.insertBefore(wf, s);
})(document);
