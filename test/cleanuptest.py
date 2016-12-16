from seecr.test import SeecrTestCase
from os import makedirs
from os.path import join, isfile
from seecrdeps import cleanup

class CleanUpTest(SeecrTestCase):

    def testCleanUp(self):
        makedirs(join(self.tempdir, "folder"))
        pycFile = join(self.tempdir, "folder", "blah.pyc")
        pyFile = join(self.tempdir, "folder", "blah.py")
        for f in [pyFile, pycFile]:
            open(f, "w").write("")
        self.assertTrue(isfile(pyFile))
        self.assertTrue(isfile(pycFile))

        cleanup(self.tempdir)
        self.assertTrue(isfile(pyFile))
        self.assertFalse(isfile(pycFile))

