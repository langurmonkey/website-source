minify:
  $WEB/scripts/minify-all.sh theme-bw

hugo: minify
  hugo --destination "$WEB/public" --minify --quiet

alias generate := pagefind
pagefind: hugo
  npx pagefind --site "$WEB/public"

deploy: stop pagefind 
  $WEB/deploy.sh

# Serve the hugo site locally in http://localhost:1313
serve: pagefind
    HUGO_BASEURL="http://localhost:1313/" nohup hugo server 2>&1 1>/dev/null &

# Stop the local server
stop:
    pkill hugo || true

# Cleans the generated site
clean:
    rm -rf public/*


thumbsup:
  $WEB/thumbsup-run.sh
