import os
from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, patch

class ProjConan(ConanFile):
    name = "paraview"
    description = """ParaView is an open-source, multi-platform data analysis and visualization application."""
    version = "5.5.2"
    settings = "os"
    url="https://www.paraview.org/"
    license="GPL"
    exports_sources = ['patches/*']


    def requirements(self):
        self.requires("qt/5.13.2@bincrafters/stable")

        self.options["qt"].qttools=True
        self.options["qt"].qtxmlpatterns=True
        self.options["qt"].qtsvg=True


    def source(self):

        filename = 'ParaView-v%s.tar.xz' % self.version

        tools.get(**self.conan_data["sources"][self.version],filename=filename)
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def configure_cmake(self):
        cmake = CMake(self)
        
        # if self.settings.os == "Macos":
        cmake.definitions["MACOSX_APP_INSTALL_PREFIX"]="bin"

        cmake.configure(source_folder="Paraview-v%s" % self.version)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        
    def deploy(self):
        self.copy("./bin/*")
        

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy("*", dst="bin", src="bin")
        self.copy("*.dylib", dst="lib", src="lib")
        self.copy("*.so", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.name = "PV" #don't clash with the built in cmake FindParaview if we need it later

