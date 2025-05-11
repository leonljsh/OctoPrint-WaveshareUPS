$(function() {
    function WaveshareUPSViewModel(parameters) {
        var self = this;

        // Observable data
        self.battery_percentage = ko.observable(0);
        self.power_supply_status = ko.observable('Unknown');
        self.load_voltage = ko.observable(0);
        self.psu_voltage = ko.observable(0);
        self.shunt_voltage = ko.observable(0);
        self.current = ko.observable(0);
        self.power = ko.observable(0);
        self.remaining_runtime = ko.observable(0);

        // Computed values
        self.iconClass = ko.pureComputed(function () {
            if (self.power_supply_status() === "Battery") {
                var pct = self.battery_percentage();
                if (pct > 75) return "fas fa-battery-full";
                if (pct > 50) return "fas fa-battery-three-quarters";
                if (pct > 25) return "fas fa-battery-half";
                if (pct > 10) return "fas fa-battery-quarter";
                return "fas fa-battery-empty text-error";
            }
            return "fas fa-plug text-success";
        });

        self.batteryColor = ko.pureComputed(function() {
            var pct = self.battery_percentage();
            if (pct <= 10) return '#d9534f';
            if (pct <= 30) return '#f0ad4e';
            return '#5cb85c';
        });

        self.formattedBattery = ko.pureComputed(function() {
            return Math.round(self.battery_percentage()) + '%';
        });

        self.formattedTooltip = ko.pureComputed(function() {
            return `
                <div class="ups-tooltip">
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Battery:</span>
                        <span class="ups-tooltip-value">${self.formattedBattery()}</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Status:</span>
                        <span class="ups-tooltip-value">${self.power_supply_status()}</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Voltage:</span>
                        <span class="ups-tooltip-value">${self.load_voltage().toFixed(2)} V</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Current:</span>
                        <span class="ups-tooltip-value">${Math.abs(self.current()).toFixed(1)} mA ${self.current() > 0 ? '↑' : '↓'}</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Power:</span>
                        <span class="ups-tooltip-value">${self.power().toFixed(2)} W</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">PSU:</span>
                        <span class="ups-tooltip-value">${self.psu_voltage().toFixed(2)} V</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Shunt:</span>
                        <span class="ups-tooltip-value">${self.shunt_voltage().toFixed(3)} V</span>
                    </div>
                    <div class="ups-tooltip-row">
                        <span class="ups-tooltip-label">Runtime:</span>
                        <span class="ups-tooltip-value">${Math.round(self.remaining_runtime())} min</span>
                    </div>
                </div>
            `;
        });

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "waveshareups") return;

            if (data.battery_percentage !== undefined)
                self.battery_percentage(data.battery_percentage);
            if (data.power_supply_status !== undefined)
                self.power_supply_status(data.power_supply_status);
            if (data.load_voltage !== undefined)
                self.load_voltage(data.load_voltage);
            if (data.current !== undefined)
                self.current(data.current);
            if (data.power !== undefined)
                self.power(data.power);
            if (data.psu_voltage !== undefined)
                self.psu_voltage(data.psu_voltage);
            if (data.shunt_voltage !== undefined)
                self.shunt_voltage(data.shunt_voltage);
            if (data.remaining_runtime !== undefined)
                self.remaining_runtime(data.remaining_runtime);

            $('.waveshare-ups-widget')
                .attr('data-original-title', self.formattedTooltip())
                .tooltip('fixTitle');
        };

        self.onStartupComplete = function() {
            $('.waveshare-ups-widget').tooltip({
                html: true,
                placement: 'bottom',
                trigger: 'hover'
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: WaveshareUPSViewModel,
        dependencies: ["loginStateViewModel"],
        elements: [".waveshare-ups-container"]
    });
});
