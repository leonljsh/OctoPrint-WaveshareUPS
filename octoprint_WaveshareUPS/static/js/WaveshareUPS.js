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

            // Update tooltip with formatted numbers and HTML line breaks
            var tooltipContent = "Battery: " + self.battery_percentage().toFixed(1) + "%<br>" +
                                 "Status: " + self.power_supply_status() + "<br>" +
                                 "Runtime: " + self.remaining_runtime().toFixed(1) + " mins<br>" +
                                 "PSU Voltage: " + self.psu_voltage().toFixed(3) + " V<br>" +
                                 "Shunt Voltage: " + self.shunt_voltage().toFixed(3) + " mV<br>" +
                                 "Load Voltage: " + self.load_voltage().toFixed(3) + " V<br>" +
                                 "Current: " + self.current().toFixed(3) + " mA<br>" +
                                 "Power: " + self.power().toFixed(3) + " W";

            $("#navbar_plugin_waveshareups span").attr("title", tooltipContent).tooltip('fixTitle').tooltip({html: true});
        };

        // Initialize tooltips
        self.onStartupComplete = function() {
            $('#navbar_plugin_waveshareups span').tooltip({
                placement: 'bottom',
                html: true
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: WaveshareUPSViewModel,
        dependencies: [],
        elements: ["#navbar_plugin_waveshareups"]
    });
});