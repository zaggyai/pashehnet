"""
The `pashehnet` package structure reflects the high level architecture of the
simulated sensor network.  The concepts of **sources**, **transforms**, and
**formats** are where the magic happens, providing flexibility to create a wide
variety of networks and tailor the simulation to your needs.

Sources
-------

These modules provide the source data for the simulated sensors.  Based on a
simple iterator model, they are initialized and then do nothing but return the
next value available in a steady stream.

Each sensor only has one source.

Transforms
----------

These modules provide the ability to "fiddle" with the data (or in ML parlance,
"augment") to simulate externalities affecting the pure data stream.  Things
like dropping out sensors, sensors getting "stuck" in position, or noise would
be provided by a transform.

Zero, one or more transforms can be applied to a sensor.

Formatters
----------

Formatters provide the final payload to be published.  These allow for
everything from a simple string representation of the final value to complex
JSON-packaged payloads.

Each sensor only has one formatter.

Customization
-------------

Each of the `pashehnet.sensors.sources`, `pashehnet.sensors.formats`, and
`pashehnet.sensors.transforms` packages provides a base class that you can
subclass custom components from.  You can also always subclass a core class and
override its behaviors using normal Pythonic coding practices.
"""
from .cli import cli_main  # noqa: F401
from .sensors import sources, transforms, formats, Sensor  # noqa: F401
