import os
from conans import ConanFile, CMake, tools, RunEnvironment

class SociTestConan(ConanFile):
    requires = "catch/1.5.0@TyRoXx/stable"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(os.path.join("bin", "test-empty dummy"))
