import os
from conans import ConanFile, CMake, tools, RunEnvironment

class SociTestConan(ConanFile):
    user = os.getenv("CONAN_USERNAME", "akazantsev")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "SOCI/4.0.0@{}/{}".format(user, channel), \
               "catch/1.5.0@TyRoXx/stable"
    settings = "os", "compiler", "arch", "build_type"
    default_options = "SOCI:with_postgresql=True"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        env = RunEnvironment(self)
        with tools.environment_append(env.vars):
            self.run(os.path.join("bin", "test-empty dummy"))
