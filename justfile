css:
  $WEB/scripts/minify-all.sh theme-bw

deploy: css
  $WEB/deploy.sh

hugo:
  hugo server
