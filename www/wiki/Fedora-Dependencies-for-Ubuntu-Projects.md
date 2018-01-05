# Fedora Dependencies for Ubuntu Projects

A lot of projects list Debian/Ubuntu dependencies and not Fedora/RHEL ones, so these are where I keep my list of Fedora dependencies for such projects.

# Game Engines

## Engo (Go)

Engo is a 2D game engine written in Go.

```bash
sudo dnf install openal-soft-devel mesa-libGLU-devel freeglut-devel \
    libX11-devel xrandr-devel libXcursor-devel libXinerama-devel libXi-devel
go get -u engo.io/engo
```