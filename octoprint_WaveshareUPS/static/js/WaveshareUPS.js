$(function() {
    function WaveshareUPSViewModel(parameters) {
        var self = this;

        self.battery_percentage = ko.observable();
        self.power_supply_status = ko.observable();
        self.remaining_runtime = ko.observable();
        self.psu_voltage = ko.observable();
        self.shunt_voltage = ko.observable();
        self.load_voltage = ko.observable();
        self.current = ko.observable();
        self.power = ko.observable();

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "waveshareups") {
                return;
            }

            self.battery_percentage(data.battery_percentage);
            self.power_supply_status(data.power_supply_status);
            self.remaining_runtime(data.remaining_runtime);
            self.psu_voltage(data.psu_voltage);
            self.shunt_voltage(data.shunt_voltage);
            self.load_voltage(data.load_voltage);
            self.current(data.current);
            self.power(data.power);

            var iconClass;
            if (self.power_supply_status() === "Battery") {
                if (self.battery_percentage() > 75) {
                    iconClass = "fas fa-battery-full";
                } else if (self.battery_percentage() > 50) {
                    iconClass = "fas fa-battery-three-quarters";
                } else if (self.battery_percentage() > 25) {
                    iconClass = "fas fa-battery-half";
                } else if (self.battery_percentage() > 10) {
                    iconClass = "fas fa-battery-quarter";
                } else {
                    iconClass = "fas fa-battery-empty";
                }
            } else {
                iconClass = "fas fa-plug";
            }

            $("#navbar_plugin_waveshareups i").attr("class", iconClass);

            // Update tooltip
            var tooltipContent = "Battery: " + self.battery_percentage() + "%\n" +
                                 "Status: " + self.power_supply_status() + "\n" +
                                 "Runtime: " + self.remaining_runtime() + " mins\n" +
                                 "PSU Voltage: " + self.psu_voltage() + " V\n" +
                                 "Shunt Voltage: " + self.shunt_voltage() + " mV\n" +
                                 "Load Voltage: " + self.load_voltage() + " V\n" +
                                 "Current: " + self.current() + " mA\n" +
                                 "Power: " + self.power() + " W";

            $("#navbar_plugin_waveshareups span").attr("title", tooltipContent).tooltip('fixTitle');
        };

    }

    OCTOPRINT_VIEWMODELS.push({
        construct: WaveshareUPSViewModel,
        dependencies: [],
        elements: ["#navbar_plugin_waveshareups"]
    });
});