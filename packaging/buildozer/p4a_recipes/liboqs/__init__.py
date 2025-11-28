from pythonforandroid.recipe import Recipe
from pythonforandroid.toolchain import sh, shprint
from pythonforandroid.util import current_directory, ensure_dir
import os
from os.path import exists, join
from multiprocessing import cpu_count


class LiboqsRecipe(Recipe):
    name = "liboqs"
    version = "0.15.0"
    url = (
        "https://github.com/open-quantum-safe/liboqs/archive/refs/tags/{version}.tar.gz"
    )
    # optional: if you compute md5/sha256 for the zip, you can set md5sum or sha256sum
    # md5sum = '...'

    # No Python-level dependencies
    depends = ["openssl"]
    conflicts = []
    built_libraries = {"liboqs.so": "install_target/lib"}
    # Ensure we build for each architecture once

    def should_build(self, arch):
        libdir = join(self.get_build_dir(arch.arch), "..", "..", "libs", arch.arch)
        libs = ["liboqs.so"]
        return not all(exists(join(libdir, x)) for x in libs)

    def get_openssl_dir(self, arch):
        openssl_recipe = self.get_recipe("openssl", self.ctx)
        openssl_dir = openssl_recipe.get_build_dir(arch.arch)
        return openssl_dir

    def get_recipe_env(self, arch, **kwargs):
        """Set custom environment variables."""
        env = super().get_recipe_env(arch, **kwargs)
        openssl_dir = self.get_openssl_dir(arch)
        print(f"OPENSSL_DIR: {openssl_dir}")
        env["OPENSSL_ROOT_DIR"] = openssl_dir
        env["OPENSSL_INCLUDE_DIR"] = openssl_dir
        os.environ["OPENSSL_ROOT_DIR"] = openssl_dir
        os.environ["OPENSSL_INCLUDE_DIR"] = openssl_dir
        return env

    def build_arch(self, arch):
        source_dir = self.get_build_dir(arch.arch)
        build_target = join(source_dir, "build_target")
        install_target = join(source_dir, "install_target")
        ensure_dir(build_target)

        env = self.get_recipe_env(arch)

        openssl_dir = self.get_openssl_dir(arch)
        with current_directory(build_target):
            shprint(
                sh.cmake,
                source_dir,
                "-DANDROID_ABI={}".format(arch.arch),
                "-DANDROID_NATIVE_API_LEVEL={}".format(self.ctx.ndk_api),
                "-DANDROID_STL=" + self.stl_lib_name,
                "-DCMAKE_TOOLCHAIN_FILE={}".format(
                    join(self.ctx.ndk_dir, "build", "cmake", "android.toolchain.cmake")
                ),
                "-DCMAKE_INSTALL_PREFIX={}".format(install_target),
                "-DCMAKE_BUILD_TYPE=Release",
                "-DBUILD_SHARED_LIBS=ON",
                "-DOQS_BUILD_ONLY_LIB=ON",
                f"-DCMAKE_FIND_ROOT_PATH={openssl_dir}",
                "-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY",
                "-DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY",
                f"-DOPENSSL_ROOT_DIR={openssl_dir}",
                "-DOPENSSL_USE_STATIC_LIBS=FALSE",
                "-DOPENSSL_INCLUDE_DIR={}/include".format(openssl_dir),
                "-DOPENSSL_LIBRARIES={}/libcrypto.so;{}/libssl.so".format(
                    openssl_dir, openssl_dir
                ),
                f"-DOPENSSL_CRYPTO_LIBRARY={openssl_dir}/libcrypto.so",
                f"-DOPENSSL_SSL_LIBRARY={openssl_dir}/libssl.so",
                _env=env,
            )
            shprint(sh.make, "-j" + str(cpu_count()), _env=env)

            # We make the install because this way we will have all the
            # includes in one place
            shprint(sh.make, "install", _env=env)

    # Optionally implement postbuild_arch to clean up or move files.


recipe = LiboqsRecipe()
