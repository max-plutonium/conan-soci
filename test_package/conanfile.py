from conans import ConanFile, CMake, tools
import os

class TestSociConan(ConanFile):
    requires = "SOCI/3.2.3@laeknaromur/stable"
    default_options = "SOCI:with_postgresql=True"

    def test(self):
        # nnop
        self.output.warn("doing nothing...")
