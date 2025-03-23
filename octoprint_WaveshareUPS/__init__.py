import octoprint.plugin
from .external.INA219 import INA219  # Import the INA219 class from the external directory
import threading
import time

class WaveshareUPSPlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.TemplatePlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        self._address = 0x42  # Address of the INA219 sensor
        self._battery_percentage = 0
        self._power_supply_status = "Unknown"
        self._remaining_runtime = 0
        self._critical_threshold = 10  # Critical battery percentage threshold
        self._stop_thread = False
        
        # Initialize values for additional metrics
        self._psu_voltage = 0
        self._shunt_voltage = 0
        self._load_voltage = 0
        self._current = 0
        self._power = 0

    def on_after_startup(self):
        self._logger.info("Waveshare UPS Plugin started")
        threading.Thread(target=self._update_ups_status).start()

    def _update_ups_status(self):
        # Log the message content
        self._logger.info("Starting UPS status update thread")

        ina219 = INA219(addr=self._address)
        while not self._stop_thread:
            try:
                self._load_voltage = ina219.getBusVoltage_V()  # Voltage on V- (load side)
                self._shunt_voltage = ina219.getShuntVoltage_mV() / 1000  # Voltage between V+ and V- across the shunt
                self._psu_voltage = self._load_voltage + self._shunt_voltage
                self._current = ina219.getCurrent_mA()  # Current in mA
                self._power = ina219.getPower_W()  # Power in W

                # Calculate battery percentage
                self._battery_percentage = (self._load_voltage - 6) / 2.4 * 100
                if self._battery_percentage > 100:
                    self._battery_percentage = 100
                if self._battery_percentage < 0:
                    self._battery_percentage = 0

                # Determine power supply status
                if self._current > 0:  # Positive current indicates charging
                    self._power_supply_status = "Power Supply"
                else:  # Negative current indicates discharging
                    self._power_supply_status = "Battery"

                # Estimate remaining runtime (this is a placeholder, adjust as needed)
                self._remaining_runtime = (self._battery_percentage / 100) * 120  # Assume 120 minutes at full charge

                # Send notification if battery is below critical threshold
                if self._power_supply_status == "Battery" and self._battery_percentage <= self._critical_threshold:
                    self._send_critical_notification()

                # Update the UI
                self._plugin_manager.send_plugin_message(self._identifier, dict(
                    battery_percentage=self._battery_percentage,
                    power_supply_status=self._power_supply_status,
                    remaining_runtime=self._remaining_runtime,
                    psu_voltage=self._psu_voltage,
                    shunt_voltage=self._shunt_voltage,
                    load_voltage=self._load_voltage,
                    current=self._current,
                    power=self._power
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
        return dict(
            js=["js/WaveshareUPS.js"],
            css= ["css/WaveshareUPS.css"]
        )

    def on_api_get(self, request):
        return flask.jsonify(  # type: ignore
            battery_percentage=self._battery_percentage,
            power_supply_status=self._power_supply_status,
            remaining_runtime=self._remaining_runtime,
            psu_voltage=self._psu_voltage,
            shunt_voltage=self._shunt_voltage,
            load_voltage=self._load_voltage,
            current=self._current,
            power=self._power
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

__plugin_pythoncompat__ = ">=3,<4"
