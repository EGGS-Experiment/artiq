#!/usr/bin/env python3

"""
Set entry points for using artiq when installed from source.
"""

from setuptools import setup, find_packages

console_scripts = [
    "artiq_client = artiq.frontend.artiq_client:main",
    "artiq_compile = artiq.frontend.artiq_compile:main",
    "artiq_coreanalyzer = artiq.frontend.artiq_coreanalyzer:main",
    "artiq_coremgmt = artiq.frontend.artiq_coremgmt:main",
    "artiq_ddb_template = artiq.frontend.artiq_ddb_template:main",
    "artiq_master = artiq.frontend.artiq_master:main",
    "artiq_mkfs = artiq.frontend.artiq_mkfs:main",
    "artiq_rtiomon = artiq.frontend.artiq_rtiomon:main",
    "artiq_sinara_tester = artiq.frontend.artiq_sinara_tester:main",
    "artiq_session = artiq.frontend.artiq_session:main",
    "artiq_route = artiq.frontend.artiq_route:main",
    "artiq_run = artiq.frontend.artiq_run:main",
    "artiq_flash = artiq.frontend.artiq_flash:main",
    "aqctl_corelog = artiq.frontend.aqctl_corelog:main",
    "aqctl_moninj_proxy = artiq.frontend.aqctl_moninj_proxy:main",
    "afws_client = artiq.frontend.afws_client:main",
]

gui_scripts = [
    "artiq_browser = artiq.frontend.artiq_browser:main",
    "artiq_dashboard = artiq.frontend.artiq_dashboard:main",
]

setup(
    name="artiq_lax",
    version='0.0.1',
    extras_require={},
    namespace_packages=[],
    ext_modules=[],
    entry_points={
        "console_scripts": console_scripts,
        "gui_scripts": gui_scripts
    }
)
