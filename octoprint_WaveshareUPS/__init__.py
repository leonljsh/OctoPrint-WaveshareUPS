import octoprint.plugin
from smbus2 import SMBus  # Updated to use smbus2
import threading
import time

class WaveshareUPSPlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.TemplatePlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        self._bus = SMBus(1)
        self._address = 0x42  # Address of the INA219 sensor
        self._battery_percentage = 0
        self._power_supply_status = "Unknown"
        self._remaining_runtime = 0
        self._critical_threshold = 10  # Critical battery percentage threshold
        self._stop_thread = False

    def on_after_startup(self):
        self._logger.info("Waveshare UPS Plugin started")
        threading.Thread(target=self._update_ups_status).start()

    def _update_ups_status(self):
        ina219 = INA219(addr=self._address)
        while not self._stop_thread:
            try:
                bus_voltage = ina219.getBusVoltage_V()  # Voltage on V- (load side)
                shunt_voltage = ina219.getShuntVoltage_mV() / 1000  # Voltage between V+ and V- across the shunt
                current = ina219.getCurrent_mA()  # Current in mA
                power = ina219.getPower_W()  # Power in W

                # Calculate battery percentage
                self._battery_percentage = (bus_voltage - 6) / 2.4 * 100
                if self._battery_percentage > 100:
                    self._battery_percentage = 100
                if self._battery_percentage < 0:
                    self._battery_percentage = 0

                # Determine power supply status
                self._power_supply_status = "Battery" if bus_voltage < 12 else "Power Supply"

                # Estimate remaining runtime (this is a placeholder, adjust as needed)
                self._remaining_runtime = (self._battery_percentage / 100) * 120  # Assume 120 minutes at full charge

                # Send notification if battery is below critical threshold
                if self._power_supply_status == "Battery" and self._battery_percentage <= self._critical_threshold:
                    self._send_critical_notification()

                # Update the UI
                self._plugin_manager.send_plugin_message(self._identifier, dict(
                    battery_percentage=self._battery_percentage,
                    power_supply_status=self._power_supply_status,
                    remaining_runtime=self._remaining_runtime
                ))

                time.sleep(10)
            except Exception as e:
                self._logger.error("Error reading from UPS HAT: {}".format(str(e)))
                time.sleep(10)

    def _send_critical_notification(self):
        self._plugin_manager.send_plugin_message(self._identifier, dict(
            type="critical",
            message="Battery level critical: {}% remaining".format(self._battery_percentage)
        ))

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "WaveshareUPS": {
                "displayName": "Waveshareups Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "michaelszubartowicz",
                "repo": "OctoPrint-WaveshareUPS",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/michaelszubartowicz/OctoPrint-WaveshareUPS/archive/{target_version}.zip",
            }
        }

    def get_template_configs(self):
        return [dict(type="navbar", custom_bindings=False, template="waveshareups_navbar.jinja2")]

    def get_assets(self):
        return dict(js=["js/waveshareups.js", "css/waveshareups.css"])

    def on_api_get(self, request):
        return flask.jsonify(
            battery_percentage=self._battery_percentage,
            power_supply_status=self._power_supply_status,
            remaining_runtime=self._remaining_runtime
        )

    def on_shutdown(self):
        self._stop_thread = True

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = WaveshareUPSPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

__plugin_name__ = "Waveshare UPS Plugin"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_version__ = "0.1.0"
