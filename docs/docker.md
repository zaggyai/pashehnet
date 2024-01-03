# PashehNet in Docker

The container is intended to make getting PashehNet up and running quickly with only a config file and Docker.

The latest image can be found on Docker Hub under [zaggyai/pashehnet](https://hub.docker.com/repository/docker/zaggyai/pashehnet).

A sample config file posting to the Mosquitto test server:

```yaml
version: 1
target:
  resource: MQTTTarget
  spec:
    hostname: test.mosquitto.org
sensors:
  - topic: pashehnet/testing/sensor1
    id: 'sensor1'
    frequency: 1
    source:
      resource: SawtoothWaveSource
      spec:
        frequency: 5
        sample_rate: 10
        width: 0.5
    format:
      resource: SimpleFormat
```

Sample Dockerfile to build a new container and copy this config into it:

```dockerfile
FROM zaggyai/pashehnet:latest
ADD config.yaml .
```

This container can also be run standalone by passing the config file via the command line:

```bash
docker run --rm -v ./:/config zaggyai/pashehnet:latest --config /config/config.yaml
```