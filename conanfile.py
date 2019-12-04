import os
from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, patch

class ProjConan(ConanFile):
    name = "paraview"
    description = """ParaView is an open-source, multi-platform data analysis and visualization application."""
    version = "5.5.2"
    generators = "cmake"
    settings = "os"
    url="https://www.paraview.org/"
    license="GPL"
    exports_sources = ['patches/*']



    def requirements(self):
        self.requires("qt/5.13.2@bincrafters/stable")

        self.options["qt"].qttools=True
        self.options["qt"].qtxmlpatterns=True

    def source(self):

        zip_name ="ParaView-v5.5.2.zip"
        download("https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.5&type=source&os=Sources&downloadFile=%s"%zip_name,zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)

    def configure_cmake(self):
        cmake = CMake(self)
        
        # if self.settings.os == "Macos":
        cmake.definitions["MACOSX_APP_INSTALL_PREFIX"]="app"

        cmake.configure(source_folder="Paraview-v%s" % self.version)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        
        

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        self.copy("*", dst="bin", src="bin")
        self.copy("*", dst="app", src="app")
        self.copy("*.dylib", dst="lib", src="lib")
        # self.copy("*.lib", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)


