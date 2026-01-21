# Run the minify script.
minify:
  $WEB/scripts/minify-all.sh theme-bw

# Run hugo. This is not a final target! To generate the site
# use 'generate'.
hugo: minify
  hugo --destination "$WEB/public" --minify --quiet

# Generate the static site offline.
alias generate := pagefind
# Run the site generation and the pagefind post-hook.
pagefind: hugo
  npx pagefind --site "$WEB/public"

# Generate and deploy the site to NFS.
deploy: stop pagefind 
  $WEB/deploy.sh

# Serve the hugo site locally in http://localhost:1313
serve: pagefind
    HUGO_BASEURL="http://localhost:1313/" nohup hugo server 2>&1 1>/dev/null &

# Stop the local server.
stop:
    pkill hugo || true

# Cleans the generated site.
clean:
    rm -rf public/*

# Generate the photo gallery with thumbsup.
thumbsup:
  $WEB/thumbsup-run.sh
