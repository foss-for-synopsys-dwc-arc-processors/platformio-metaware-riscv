# Metaware Risc-V: development platform for [PlatformIO](https://platformio.org)
[![Build Status](https://github.com/platformio/platform-metaware_riscv/workflows/Examples/badge.svg)](https://github.com/platformio/platform-metaware_riscv/actions)

The Metaware Risc-V is the latest ARC Metaware Risc-V series. 

* [Home](https://registry.platformio.org/platforms/platformio/metaware_riscv) (home page in PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/metaware_riscv.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = metaware_riscv
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-metaware_riscv.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/metaware_riscv.html).
