# pymainichigo

`pymainichigo` is a wallpaper generator for the game of [Go](https://en.wikipedia.org/wiki/Go_(game)). It can be configured to generate a new wallpaper every minute so that your desktop plays out an SGF over the course of an entire day. It aims to be customizable and beautiful.

## Dependencies

`pymainichigo` itself requires Python ≥ 3.2. Individual renderers and/or SGF selectors may have additional dependencies. **In particular**, the only renderer that works at the moment has a hard dependency on [Processing](https://processing.org/), which must be installed separately. I am working on other renderers that use pure Python to ease this dependency (and would welcome contributions of such as well).

`pymainichigo` works well on macOS and the majority of Linux desktop and window managers. In theory it should work fine on Windows as well, but I haven't tested that at all yet.

## Installation

Assuming you have a working Python/pip environment, simply type:
```
$ pip install pymainichigo
```

## Configuration

`pymainichigo` is controlled through a `config.yaml` file located (by default) at `~/.pymainichigo/config.yaml`. The default `config.yaml` looks like:

```yaml
wallpaper:
  width: 1920
  height: 1080
  output: ~/.pymainichigo/wallpaper.png
sgf:
- file:
    path: <path to package>/test.sgf
render:
- processing:
```
