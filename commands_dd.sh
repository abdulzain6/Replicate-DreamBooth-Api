docker run -d -v --net=host /var/run/docker.sock:/var/run/docker.sock:ro \
          -v /proc/:/host/proc/:ro \
          -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
          -p 127.0.0.1:8126:8126/tcp \
          -e DD_API_KEY=<YOUR_API_KEY> \
          datadog/agent:latest

docker run -d --net=host \
          -e REPLICATE_TOKEN=...\
          registry.digitalocean.com/anyscale/replicate_api:latest