
---

My website project. Visit it in [jumpinglangur.gitlab.io](http://jumpinglangur.gitlab.io).

To renew the certificate, just do:

```
$  sudo certbot certonly --manual -d tonisagrista.com
```

Then go to the [repo configuration](https://gitlab.com/jumpinglangur/jumpinglangur.gitlab.io/pages)
and update the certificate and key with `/etc/letsencrypt/live/tonisagrista.com/fullchain.pem` and
`/etc/letsencrypt/live/tonisagrista.com/privkey.pem` respectively.

---
