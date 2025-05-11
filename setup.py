# coding=utf-8
import octoprint_setuptools
from setuptools import setup

plugin_identifier = "waveshareups"
plugin_package = "octoprint_WaveshareUPS"
plugin_name = "Waveshare UPS HAT Support"
plugin_version = "0.1.1"
plugin_description = "An OctoPrint plugin to support the Waveshare UPS HAT (D)"
plugin_author = "Leonid Shekhtman"
plugin_author_email = "leon.ljsh@gmail.com"
plugin_url = "https://github.com/leonljsh/OctoPrint-WaveshareUPS/"
plugin_license = "MIT"
plugin_requires = ["smbus"]

plugin_additional_data = []
plugin_additional_packages = []
plugin_ignored_packages = []
additional_setup_parameters = {
    "python_requires": ">=3,<4"
}

setup_parameters = octoprint_setuptools.create_plugin_setup_parameters(
    identifier="waveshareups",
    package="octoprint_WaveshareUPS",
    name="Waveshare UPS HAT Support",
    version="0.1.1",
    description="An OctoPrint plugin to support the Waveshare UPS HAT (D)",
    author="Leonid Shekhtman",
    mail="leon.ljsh@gmail.com",
    url="https://github.com/leonljsh/OctoPrint-WaveshareUPS/",
    license="MIT",
    requires=["smbus2"],
    additional_packages=[],
    ignored_packages=[],
    additional_data=[],
)

setup(**setup_parameters)
