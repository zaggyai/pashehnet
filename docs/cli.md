# Command Line Interface

**PashehNet** provides a command line interface (CLI) that can be leveraged to launch a simulated sensor network (SSN) 
from a YAML config file, with no application coding required.

## Using the CLI

```bash
NAME
    pashehnet - Provides a wrapper to create the network and kick off the simulation from a command line interface

SYNOPSIS
    pashehnet - COMMAND | VALUE

DESCRIPTION
    Provides a wrapper to create the network and kick off the simulation from a command line interface

COMMANDS
    COMMAND is one of the following:

     check
       Load and validate network configuration, without creating or running it

     run
       Create and run the network simulation

VALUES
    VALUE is one of the following:

     CURRENT_CONFIG_VERSION

     DEFAULT_CONFIG_FNAME

     config_file
```

The `check` command is used to validate a config file without starting the SSN.  If it succeeds, there should be no output; if it fails it will report what is incorrect.

The `run` command is used to start the SSN defined in the config file; it can 
be stopped by hitting `Ctrl-C` or killing the parent process with a `SIGTERM` 
or `SIGKILL` signal.

## Config file

The config file is defined using [YAML](https://yaml.org/) which is a 
relatively easy to use hierachical file format.  The core components of the file are:

```yaml
version: 1

target:
  resource: <target-resource-name>
  spec: {}

sensors:
  - topic: <topic-channel-name>
    id: <sensor-id>

    source:
      resource: <source-resource-name>
      spec: {}

    transforms:
      - resource: <transform-resource-name>
        spec: {}

    format:
      resource: <format-resource-name>
      spec: {}
```

`version` is currently set to 1.  Any other value will fail validation.

`target` defines the target system to publish sensor data to.  The key 
`resource` is simply the class name of the target you 
want to use for the network; refer to the API reference for available classes. The 
`spec` element contains the target config information; the keys map 
1:1 to the class constructor parameters. If there are no constructor params or 
you're fine with the defaults, `spec` is optional. There can be only one per SSN.

`sensors` is a list of sensor definitions the SSN is constructed from.  The keys
`topic`, `id`, `source` and `format` are the only required elements.  Sampling 
speed can be set in Hz using the optional `frequency` key; default sampling is 
at 1Hz.

### Sensor definitions

The SSN can declare one or more sensors; just keep adding items under the `sensors` list.

`source` declares a `resource` which is simply the class name of the source you 
want to use for the sensor; refer to the API reference for available classes. The 
`spec` element contains the source config information; the keys map 
1:1 to the class constructor parameters. If there are no constructor params, or 
you're fine with the defaults, `spec` is optional.  There can be only one per sensor.

`transforms` is an optional configuration item that provides a list of 
transformations that will be applied to the data read from `source` in the 
order they are declared.  The key `resource` is simply the class name of the transform you 
want to use for the sensor; refer to the API reference for available classes. The 
`spec` element contains the transform config information; the keys map 
1:1 to the class constructor parameters. If there are no constructor params, or 
you're fine with the defaults, `spec` is optional.

`format` declares a `resource` which is simply the class name of the formatter you 
want to use for the sensor; refer to the API reference for available classes. The 
`spec` element contains the formatter config information; the keys map 
1:1 to the class constructor parameters. If there are no constructor params, or 
you're fine with the defaults, `spec` is optional.  There can be only one per sensor.

### Sample config file

```{code-block} yaml
:caption: config.yml

version: 1
target:
  resource: MQTTTarget
  spec:
    hostname: $MQTT_HOST
    port: $MQTT_PORT
    username: $MQTT_USER
    password: $MQTT_PWD
    protocol: $MQTT_PROTOCOL|MQTTv311
sensors:
  - topic: pashehnet.testing.squarewavesource
    id: 'squarewavesource'
    frequency: 2
    source:
      resource: SquareWaveSource
      spec:
        frequency: 5
        sample_rate: 500
        duty_cycle: 0.5
    format:
      resource: SimpleFormat
```

See that we're using an `MQTTTarget` for this SSN, and that we are able to 
embed environment variables in place of literals if you need to.  **PashehNet** 
leverages the [EnvYAML](https://github.com/thesimj/envyaml) package so any 
feature it provides is available (e.g. note the optional default for `target.spec.protocol`).

We define a single sensor with the id of `squarewavesource` and specify that it 
will be published to the `pashehnet.testing.squarewavesource` topic on the target with a frequency of 2Hz.

We're using a `SimpleFormat` formatter here which simply stringifies the value, so no `spec` section required.

No transform is defined, so the data should pass through cleanly from the source.

## Logging

Logging is configured via the `LOG_LEVEL` environment variable.  By default, 
the package output is set to `INFO`, but gives more information if `DEBUG` is set:

```{code-block} bash
:caption: Config check with LOG_LEVEL=debug

$ LOG_LEVEL=debug pashehnet check --config config.yml 
2023-12-29 17:11:52,285 [DEBUG] Starting configuration check
2023-12-29 17:11:52,285 [DEBUG] Loading configuration file: config.yml
2023-12-29 17:11:52,293 [DEBUG] version: 1
2023-12-29 17:11:52,293 [DEBUG] target: MQTTTarget
2023-12-29 17:11:52,293 [DEBUG] sensors: [{'topic': 'pashehnet.testing.squarewavesource', 'id': 'squarewavesource', 'frequency': 2, 'source': {'resource': 'SquareWaveSource', 'spec': {'frequency': 5, 'sample_rate': 500, 'duty_cycle': 0.5}}, 'format': {'resource': 'SimpleFormat'}}]
```

```{code-block} bash
:caption: Running SSN LOG_LEVEL=info

$ LOG_LEVEL=info pashehnet run --config config.yml 
2023-12-29 17:16:51,414 [INFO] Creating target from spec
2023-12-29 17:16:51,414 [INFO] Creating sensor network
2023-12-29 17:16:51,414 [INFO] Adding sensors...
2023-12-29 17:16:51,414 [INFO] Network populated, starting up...
2023-12-29 17:16:51,426 [INFO] Network running
```

```{code-block} bash
:caption: Running SSN LOG_LEVEL=debug

$ LOG_LEVEL=debug pashehnet run --config config.yml 
2023-12-29 17:17:49,735 [DEBUG] Starting runner
2023-12-29 17:17:49,735 [DEBUG] Loading configuration file: config.yml
2023-12-29 17:17:49,742 [INFO] Creating target from spec
2023-12-29 17:17:49,743 [INFO] Creating sensor network
2023-12-29 17:17:49,743 [INFO] Adding sensors...
2023-12-29 17:17:49,743 [DEBUG] Adding sensor id: squarewavesource // topic: pashehnet.testing.squarewavesource
2023-12-29 17:17:49,743 [INFO] Network populated, starting up...
2023-12-29 17:17:49,743 [DEBUG] SensorProcess starting: pashehnet.testing.squarewavesource // <pashehnet.sensors.sensor.Sensor object at 0x1401b3200>
2023-12-29 17:17:49,755 [DEBUG] Started 1 sensor processes.
2023-12-29 17:17:49,757 [INFO] Network running
2023-12-29 17:17:51,595 [DEBUG] Sensor squarewavesource sending payload 1.0 to pashehnet.testing.squarewavesource
2023-12-29 17:17:52,386 [DEBUG] Sensor squarewavesource sending payload 1.0 to pashehnet.testing.squarewavesource
2023-12-29 17:17:52,887 [DEBUG] Sensor squarewavesource sending payload 1.0 to pashehnet.testing.squarewavesource
2023-12-29 17:17:53,392 [DEBUG] Sensor squarewavesource sending payload 1.0 to pashehnet.testing.squarewavesource

# <Hitting Ctrl-C>

2023-12-29 17:17:53,609 [DEBUG] SensorProcess terminating: pashehnet.testing.squarewavesource // <pashehnet.sensors.sensor.Sensor object at 0x1401b3200>
2023-12-29 17:17:53,609 [DEBUG] SensorProcess joining: pashehnet.testing.squarewavesource // <pashehnet.sensors.sensor.Sensor object at 0x1401b3200>
2023-12-29 17:17:53,621 [DEBUG] Terminated 1 sensor processes.
```