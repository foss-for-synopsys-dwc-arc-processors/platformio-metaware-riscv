How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](https://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/platformio/platform-metaware_riscv/archive/develop.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-metaware_riscv/examples/native-helloworld

# Build project
$ pio run

# Upload firmware
$ pio run --target upload

# Build specific environment
$ pio run -e stc15w404as

# Upload firmware for the specific environment
$ pio run -e stc15w404as --target upload

# Clean build files
$ pio run --target clean
```
