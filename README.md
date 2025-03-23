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
- first public release
  
### V0.2
- add settings page to set thresholds
- add threshold and command to execute (e.g., aborting the print job and shutting down the raspberry pi when power loss is imminent)
- (optional) add graphical settings (choice of symbol and colors)

### V0.3
- change behavior of runtime estimation:
    -  only available when not plugged in
    - based as linear esimation on current (i.e., moving avg over last minute) power draw
    - intention: when a print job is running and the camera feed or gcode viewer are refreshed frequently, the power load should be reflected and considered when a power loss to the raspberry pi occurs
- compatibility with telegram plugin (send notifications, get status)

### V0.4 
- reserved for possible features and bug fixes from community

### V1.0
- feature completeness achieved ;)