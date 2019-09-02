from conans import ConanFile, CMake, tools, RunEnvironment
import os

class UasmTestConan(ConanFile):
    def test(self):
        if not tools.cross_building(self.settings):
            self.run("uasm -coff %s" % os.path.join(self.source_folder, "test32.asm"))
