minify:
  $WEB/scripts/minify-all.sh theme-bw

deploy: stop minify
  $WEB/deploy.sh

# Serve the hugo site locally in http://localhost:1313
serve:
    HUGO_BASEURL="http://localhost:1313/" nohup hugo server 2>&1 1>/dev/null &

# Stop the local server
stop:
    pkill hugo

thumbsup:
  $WEB/thumbsup-run.sh
