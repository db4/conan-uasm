import os
from conans import tools, ConanFile, MSBuild

class UasmConan(ConanFile):
    name = "uasm"
    version = "2.50"
    description = "UASM - Macro Assembler"
    url = "http://github.com/db4/conan-uasm"
    license = "Sybase Open Watcom Public License"
    settings = "os_build", "compiler", "arch_build"

    def source(self):
        tools.get("https://github.com/Terraspace/UASM/archive/v%s.zip" % self.version,
                  sha1="2c1868b383eec0389d41370bbb0f9d280edfc70c")
        os.rename("%s-%s" % (self.name.upper(), self.version), "uasm")

    def build(self):
        with tools.chdir("uasm"):
            if self.settings.os_build == "Windows":
                tools.replace_in_file("UASM.vcxproj",
                                    "<WindowsTargetPlatformVersion>10.0.14393.0</WindowsTargetPlatformVersion>",
                                    "<WindowsTargetPlatformVersion>8.1</WindowsTargetPlatformVersion>")
                with tools.vcvars(self.settings, arch="x86"):
                    msbuild = MSBuild(self)
                    msbuild.build("UASM.sln", build_type="Release", arch="x86")
            elif self.settings.os_build == "Linux":
                tools.replace_in_file("gccLinux64.mak",
                                    "CC = gcc",
                                    "CC = gcc -std=c99")
                self.run("make -f gccLinux64.mak")
            else:
                raise Exception("%s is not supported yet" % self.settings.os_build)

    def package(self):
        self.copy("License.txt")
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("uasm/GccUnixR/uasm", dst="bin", keep_path=False)

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

    def package_id(self):
        self.info.include_build_settings()
        del self.info.settings.compiler
        if self.settings.os_build == "Windows":
            del self.info.settings.arch_build
