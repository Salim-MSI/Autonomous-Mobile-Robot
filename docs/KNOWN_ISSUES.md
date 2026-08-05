# Known Issues

## WSL Address Changes

The WSL virtual IPv4 address may change after restarting Windows or WSL.

Retrieve the current address with:

```bash
hostname -I | awk '{print $1}'
```

Update the destination used by `amr_joystick_sender`.

## Empty Directories Are Not Tracked by Git

A package can build locally but fail after a clean clone if CMake installs an empty directory that Git did not track. Add a `.gitkeep` file or remove the unnecessary installation rule.

## Build Artifacts Can Hide Repository Problems

Always validate major changes with:

```bash
rm -rf build install log
colcon build --symlink-install
```

A clean clone is the preferred reproducibility test.

## Map Destination Directory

Create the destination directory before saving a map:

```bash
mkdir -p maps
```

## Workspace Setup After Failed Build

Do not source `install/setup.bash` when the build failed, because package-local setup files may be missing.
