import os

from conans import ConanFile, CMake, tools


class TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        self.requires("paraview/5.5.2@CHM/dev")

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%paraview --version" % os.sep)
