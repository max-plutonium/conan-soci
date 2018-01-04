from conans import ConanFile, CMake, tools

class SociConan(ConanFile):
    name = "SOCI"
    description = """SOCI is a database access library for C++ that makes the illusion
    of embedding SQL queries in the regular C++ code, staying entirely
    within the Standard C++."""
    version = "4.0.0"
    commit = "8b00c6bd00e5dec8dd91d42bdad3b3145ce8290f"
    license = "Boost Software License - Version 1.0"
    url = "https://github.com/akazantsev/conan-soci"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "with_db2": [True, False],
               "with_firebird": [True, False],
               "with_mysql": [True, False],
               "with_odbc": [True, False],
               "with_oracle": [True, False],
               "with_postgresql": [True, False],
               "with_sqlite3": [True, False]}
    default_options = "shared=False", "with_db2=False", "with_firebird=False",\
        "with_mysql=False", "with_odbc=False", "with_oracle=False",\
        "with_postgresql=False", "with_sqlite3=False"
    generators = "cmake"
    build_dir = "./"

    def source(self):
        tools.download(
            "https://github.com/SOCI/soci/archive/{}.zip".format(self.commit),
            "source.zip")
        tools.unzip("source.zip", ".")
        tools.replace_in_file("soci-{}/CMakeLists.txt".format(self.commit),
                              "project(SOCI)", '''project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        tools.replace_in_file("soci-{}/cmake/SociUtilities.cmake".format(self.commit),
                              "set(${OUTPUT_NAME} ${TARGET_NAME}${SUFFIX} PARENT_SCOPE)",
                              'set(${OUTPUT_NAME} ${TARGET_NAME} PARENT_SCOPE)')

    def build(self):
        cmake = CMake(self)

        cmake.definitions["WITH_DB2"] = "ON" if self.options.with_db2 else "OFF"
        cmake.definitions["WITH_FIREBIRD"] = "ON" if self.options.with_firebird else "OFF"
        cmake.definitions["WITH_MYSQL"] = "ON" if self.options.with_mysql else "OFF"
        cmake.definitions["WITH_ODBC"] = "ON" if self.options.with_odbc else "OFF"
        cmake.definitions["WITH_ORACLE"] = "ON" if self.options.with_oracle else "OFF"
        cmake.definitions["WITH_POSTGRESQL"] = "ON" if self.options.with_postgresql else "OFF"
        cmake.definitions["WITH_SQLITE3"] = "ON" if self.options.with_sqlite3 else "OFF"

        cmake.definitions["SOCI_TESTS"] = "OFF"
        cmake.definitions["SOCI_STATIC"] = "OFF" if self.options.shared else "ON"
        cmake.definitions["SOCI_SHARED"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "1" if self.options.shared else "0"
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}/install".format(self.build_dir)

        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            runtime = "/MT"
            
            if self.settings.build_type == "Debug":
                runtime = runtime + "d"
            
            cmake.definitions["CMAKE_CXX_FLAGS_DEBUG"] = runtime
            cmake.definitions["CMAKE_CXX_FLAGS_RELEASE"] = runtime

        cmake.configure(source_dir="soci-{}".format(self.commit),
                        build_dir=self.build_dir)
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/soci"]
        self.cpp_info.libs = ["soci_core", "soci_empty"]
        
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
            
        if self.options.with_db2:
            self.cpp_info.libs.append("soci_db2")

        if self.options.with_firebird:
            self.cpp_info.libs.append("soci_firebird")

        if self.options.with_mysql:
            self.cpp_info.libs.append("soci_mysql")

        if self.options.with_odbc:
            self.cpp_info.libs.append("soci_odbc")

        if self.options.with_oracle:
            self.cpp_info.libs.append("soci_oracle")

        if self.options.with_postgresql:
            self.cpp_info.libs.append("soci_postgresql")

        if self.options.with_sqlite3:
            self.cpp_info.libs.append("soci_sqlite3")

        if self.settings.os == "Windows" and not self.options.shared:
            for idx in range(len(self.cpp_info.libs)):
                self.cpp_info.libs[idx] = "lib" + self.cpp_info.libs[idx]

    def system_requirements(self):
        pass
