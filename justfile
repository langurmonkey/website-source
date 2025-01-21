minify:
  $WEB/scripts/minify-all.sh theme-bw

deploy: minify
  $WEB/deploy.sh

hugo:
  hugo server

thumbsup:
  $WEB/thumbsup-run.sh
