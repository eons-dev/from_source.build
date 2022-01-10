import os
import logging
import shutil
import jsonpickle
from distutils.file_util import copy_file
from distutils.dir_util import copy_tree, mkpath
from ebbs import Builder


# Class name is what is used at cli, so we defy convention here in favor of ease-of-use.
class from_source(Builder):
    def __init__(self, name="From Source"):
        super().__init__(name)

        self.supportedProjectTypes = []
        self.allStepsComplete = False

    # Required Builder method. See that class for details.
    def DidBuildSucceed(self):
        return self.allStepsComplete

    # Required Builder method. See that class for details.
    def Build(self):
        dirsBefore = [d for d in listdir(self.buildPath)]
        self.RunCommand(f"git clone {self.repo['url']}")
        dirsAfter = [d for d in listdir(self.buildPath)]
        newDirs = [d for d in dirsAfter if d not in dirsBefore]
        if (not len(newDirs)):
            raise OtherBuildError("Clone failed.")
        if (len(newDirs) > 1):
            newDirs = [d for d in newDirs if os.path.isdirectory(os.path.join(self.buildPath, d))]
        if (len(newDirs) > 1):
            raise OtherBuildError(f"Confused by too many options: {newDirs}")
        os.chdir(os.path.join(self.buildPath,newDirs[0]))
        mkpath("build")
        os.chdir("build")
        self.RunCommand("cmake ..")
        self.RunCommand("make")
        self.RunCommand("make install")


