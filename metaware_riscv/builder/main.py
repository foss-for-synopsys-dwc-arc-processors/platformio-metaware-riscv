# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from os.path import join

from SCons.Script import ARGUMENTS, AlwaysBuild, Default, DefaultEnvironment


def __getSize(size_type, env):
    # FIXME: i don't really know how to do this right. see:
    #        https://community.platformio.org/t/missing-integers-in-board-extra-flags-in-board-json/821
    return str(
        env.BoardConfig().get(
            "build",
            {
                # defaults
                "size_heap": 1024,
                "size_iram": 256,
                "size_xram": 65536,
                "size_code": 65536,
            },
        )[size_type]
    )


def _parseSdccFlags(flags):
    assert flags
    if isinstance(flags, list):
        flags = " ".join(flags)
    flags = str(flags)
    parsed_flags = []
    unparsed_flags = []
    prev_token = ""
    for token in flags.split(" "):
        if prev_token.startswith("--") and not token.startswith("-"):
            parsed_flags.extend([prev_token, token])
            prev_token = ""
            continue
        if prev_token:
            unparsed_flags.append(prev_token)
        prev_token = token
    unparsed_flags.append(prev_token)
    return (parsed_flags, unparsed_flags)


env = DefaultEnvironment()
platform = env.PioPlatform()
board_config = env.BoardConfig()

env.Replace(
    AR="riscv64-elf-ar",
    AS="riscv64-elf-as",
    CC="riscv64-elf-gcc",
    CXX="riscv64-elf-g++",
    GDB="riscv64-elf-gdb",
    OBJCOPY="riscv64-elf-objcopy",
    RANLIB="riscv64-elf-ranlib",
    SIZETOOL="riscv64-elf-size",



    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.text.align|\.ARC.exidx)\s+(\d+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+(\d+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    PROGSUFFIX=".elf"

)

env.Append(
    ARFLAGS=["rc"],
    ASFLAGS=["-l", "-s"],
    CFLAGS=["--specs=semihost.specs",
            "--specs=arcv.specs",
            "-mabi=ilp32",
            "-mtune=rmx100",
            "-march=rv32im_zba_zbb_zbs_zca_zcb_zcmp_zicsr",
            "-T",
            "arcv.ld",
            ],
    CCFLAGS=[
    ],
    CPPDEFINES=[],
    LINKFLAGS=["--specs=semihost.specs",
            "--specs=arcv.specs",
            "-mabi=ilp32",
            "-mtune=rmx100",
            "-march=rv32im_zba_zbb_zbs_zca_zcb_zcmp_zicsr",
            "-T",
            "arcv.ld",

    ],
)

if int(ARGUMENTS.get("PIOVERBOSE", 0)):
    env.Prepend(UPLOADERFLAGS=["-v"])

# parse manually SDCC flags
if env.get("BUILD_FLAGS"):
    _parsed, _unparsed = _parseSdccFlags(env.get("BUILD_FLAGS"))
    env.Append(CCFLAGS=_parsed)
    env["BUILD_FLAGS"] = _unparsed

project_sdcc_flags = None
if env.get("SRC_BUILD_FLAGS"):
    project_sdcc_flags, _unparsed = _parseSdccFlags(env.get("SRC_BUILD_FLAGS"))
    env["SRC_BUILD_FLAGS"] = _unparsed

#
# Target: Build executable and linkable firmware
#

target_firm = env.BuildProgram()

if project_sdcc_flags:
    env.Import("projenv")
    projenv.Append(CCFLAGS=project_sdcc_flags)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_firm, env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE")
)
AlwaysBuild(target_size)

#
# Target: Upload firmware
#

upload_protocol = env.subst("$UPLOAD_PROTOCOL")
upload_actions = []

if upload_protocol == "stcgal":
    f_cpu_khz = int(board_config.get("build.f_cpu").strip("L")) / 1000
    stcgal_protocol = board_config.get("upload.stcgal_protocol")
    env.Replace(
        UPLOADER=join(platform.get_package_dir("tool-stcgal") or "", "stcgal.py"),
        UPLOADERFLAGS=[
            "-P",
            stcgal_protocol,
            "-p",
            "$UPLOAD_PORT",
            "-t",
            int(f_cpu_khz),
            "-a",
        ],
        UPLOADCMD='"$PYTHONEXE" "$UPLOADER" $UPLOADERFLAGS $SOURCE',
    )

    upload_actions = [
        env.VerboseAction(env.AutodetectUploadPort, "Looking for upload port..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"),
    ]



# custom upload tool
elif upload_protocol == "custom":
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]

else:
    sys.stderr.write("Warning! Unknown upload protocol %s\n" % upload_protocol)

AlwaysBuild(env.Alias("upload", target_firm, upload_actions))

#
# Setup default targets
#

Default([target_buildprog, target_size])
