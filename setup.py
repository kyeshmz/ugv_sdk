from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import os
import sys
import platform
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = re.search(r"project\(ugv_sdk VERSION ([0-9.]+)\)",
                    (HERE / "CMakeLists.txt").read_text()).group(1)


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)
        super().run()

    def build_extension(self, ext):
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)
        extdir = ext_fullpath.parent.resolve()

        debug = int(os.environ.get("DEBUG", 0)
                    ) if self.debug is None else self.debug
        cfg = 'Debug' if debug else 'Release'

        cmake_args = [
            f"-DPYBIND_OUTPUT_LIBDIR={extdir}{os.sep}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DPython_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-DPYTHON_BINDING=ON"
        ]
        build_args = ['--config', cfg]
        build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())

        build_temp = Path(self.build_temp) / ext.name
        if not build_temp.exists():
            build_temp.mkdir(parents=True)
        lib_path = Path(f"{extdir}{os.sep}")
        if not lib_path.exists():
            lib_path.mkdir(parents=True)

        subprocess.run(
            ["cmake", ext.sourcedir, *cmake_args], cwd=build_temp, env=env, check=True
        )
        subprocess.run(
            ["cmake", "--build", ".", *build_args], cwd=build_temp, env=env, check=True
        )


setup(
    name='ugv_sdk_py',
    version=VERSION,
    author='Ruixiang Du (Weston Robot), with AgileX Robotics',
    author_email='ruixiang.du@westonrobot.com',
    maintainer='kyeshmz (unofficial PyPI build)',
    description='Python bindings for ugv_sdk by Weston Robot & AgileX Robotics (unofficial build)',
    long_description=(HERE / 'python' / 'PYPI_README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/westonrobot/ugv_sdk',
    project_urls={
        'Upstream': 'https://github.com/westonrobot/ugv_sdk',
        'Upstream issues': 'https://github.com/westonrobot/ugv_sdk/issues',
        'Wheel builds': 'https://github.com/kyeshmz/ugv_sdk',
    },
    license='Apache-2.0',
    license_files=['LICENSE'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    platforms=['Linux'],
    python_requires='>=3.8',
    ext_modules=[CMakeExtension('ugv_sdk_py')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    install_requires=['pybind11'],
)
