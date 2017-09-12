# pymainichigo

`pymainichigo` is a wallpaper generator for the game of [Go](https://en.wikipedia.org/wiki/Go_(game)). It can be configured to generate a new wallpaper every minute so that your desktop plays out an SGF over the course of an entire day. It aims to be customizable and beautiful.

The `processing` renderer is based on [this beautiful image](http://i.solidfiles.net/c6a7786a19.jpg) generated by [kqr](http://github.com/kqr).

## Screenshots

![](http://apetresc-screenshot.s3.amazonaws.com/2017-09-11-21:40:24.png)

![](http://apetresc-screenshot.s3.amazonaws.com/2017-09-11-21:38:25.png)

## Dependencies

`pymainichigo` itself requires Python ≥ 3.2. Individual renderers and/or SGF selectors may have additional dependencies. **In particular**, the only renderer that works at the moment has a hard dependency on [Processing](https://processing.org/) and [Xvfb](https://www.x.org/archive/X11R7.6/doc/man/man1/Xvfb.1.xhtml), which must be installed separately (they are packaged as part of most Linux distributions). I am working on other renderers that use pure Python to ease this dependency (and would welcome contributions of such as well).

`pymainichigo` works well on the majority of Linux desktop and window managers. It works on macOS and Windows as well, but because of the renderer's dependency on Processing and the lack of a headless mode on those platforms, running `pymainichigo` on them results in a Processing window flashing onto the screen before shutting down, which is annoying enough to make it unusable. Once I have a satisfactory non-Processing renderer, macOS and Windows will be supported as well.

## Installation

Assuming you have a working Python/pip environment, simply type:
```
$ pip install pymainichigo
```

Make sure Processing and Xvfb are also installed.

## Configuration

`pymainichigo` is controlled through a `config.yaml` file located (by default) at `~/.pymainichigo/config.yaml`. The default `config.yaml` looks like:

```yaml
wallpaper:
  output: "~/.pymainichigo/wallpaper.png"
  width: 1920
  height: 1080
curve: linear
sgf:
- file:
    path: "<path-to-python-package>/test.sgf"
render:
- processing:
    magnification: 5
    color: "#826904"
```

Each section is defined in more detail below.

### `wallpaper`

This section has the following attributes:
  - `output` – The file path to the generated wallpaper. If your desktop's wallpaper manager is already configured to monitor a particular file or directory for changes, you can set this to write directly there.
  - `width` and `height` – The resolution of the generated wallpaper.

### `curve`

This can be either `linear` or `sigmoid`.

In `linear` mode (the default), the SGF is played out in evenly-spaced intervals over the entire day. That is, at noon it will be exactly halfway through the SGF, at 9:00 PM it will be at 75% of the way through the SGF (since 9:00 PM is 75% of the way through the day), etc.

In `sigmoid` mode, the SGF is played out according to the sigmoid curve ![sigmoid](https://latex.codecogs.com/gif.latex?%5Cfrac%7B1%7D%7B1%20&plus;%20e%5E%7B-12x%20&plus;%206%7D%7D). This curve is calibrated so that the moves are played out very slowly prior to 9:00 AM (only ~18%) and after 9:00 PM (the last 5%); the majority of the action takes place during normal working hours.
<p align="center">
  <img src="http://apetresc-screenshot.s3.amazonaws.com/2017-09-11-20:48:36.png">
</p>

### `sgf`

This is a list of SGF selectors, to be attempted (in descending order). The first selector to return a non-empty result will be used for the day. The current set of selectors are:

#### `file`

Reads a single file off the local disk. Very boring.
  - `path` – A path to a single SGF file on disk.

#### `dir`

Randomly picks an SGF from a directory (and all of its subdirectories).
  - `path` – A path to a directory containing SGF files.

#### `rss`

Picks the latest SGF from an RSS feed containing links to SGF files as primary entries. Probably not very useful directly, but meant to be subclassed.
  - `feed_url` – The URL of an RSS feed whose entries are direct links to `.sgf` files.


#### `gokifu`
Picks the latest SGF posted to http://gokifu.com.

### `render`

This is a list of renderers, to be attempted (in descending order). The first renderer to return a non-empty result will be used. At the moment, there is only one supported selector:

#### `processing`

The Processing renderer, adapted from [kqr](http://github.com/kqr)'s [sketch](https://github.com/kqr/gists/blob/master/algorithms/proceduralgeneration/goboard.pde). Two aspects of the renderer can be customized:
  - `magnification` – A float between 0 and 10 that controls the size of the Go board in the middle of the wallpaper.
  - `color` – A 6-digit hex color code for the palette to use for the background. The default, `#826904`, exactly matches kqr's original iconic image.

## Usage

When `pymainichigo` is invoked, it generates the wallpaper according to the current time-of-day. You probably want to re-run it on a schedule so that your wallpaper updates frequently. The easiest way to do this is to just add a line like this to your crontab:

```
* * * * * DISPLAY=:0 XDG_CURRENT_DESKTOP=i3 pymainichigo
```

Do not worry about how you set the schedule, it doesn't matter - `pymainichigo` will figure out how far to progress into the SGF file according to the `curve` you set, regardless of how often it is invoked. You just need to invoke it often enough to achieve the granularity you want.

## Contributing

I welcome bug reports and pull requests (_especially_ if they implement a nice Python-only renderer!).
