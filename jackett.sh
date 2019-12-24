docker create \
  --name=jackett \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Bern \
  -p 9117:9117 \
  -v /root/jackett:/config \
  -v /mnt/Media/.download/blackhole:/downloads \
  --restart unless-stopped \
  linuxserver/jackett
