# OctoPrint-WaveshareUPS

This plugin displays a battery or power plug icon in the navigation bar. Hovering over the icon will show the current battery percentage, power supply status, and the remaining estimated runtime.

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/michaelszubartowicz/OctoPrint-WaveshareUPS/archive/master.zip


## Configuration

None. Make sure the device you are using has the Waveshare UPS Hat installed.

## Sources

- https://www.waveshare.com/wiki/UPS_HAT

## Roadmap
### V0.1
- ensure basic functionality
  
### V0.2
- add settings page to set thresholds
- add threshold and command to execute (e.g., aborting the print job and shutting down the raspberry pi when power loss is imminent)
- (optional) add graphical settings (choice of symbol and colors)
