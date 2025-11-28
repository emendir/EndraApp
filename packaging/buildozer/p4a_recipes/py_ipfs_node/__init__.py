from pythonforandroid.recipe import PythonRecipe


class PyIpfsNodeRecipe(PythonRecipe):
    version = "master"
    url = "https://github.com/emendir/py_ipfs_node/releases/download/v0.1.12rc6/ipfs_node_android_binaries.tar.gz"

    depends = ["python3", "cffi", "ipfs_tk"]
    patches = ["setup-py.patch"]

    def get_recipe_env(self, arch, **kwargs):
        """Set custom environment variables."""
        env = super().get_recipe_env(arch, **kwargs)
        env["TARGET_PLATFORM"] = "android_28_arm64_v8a"
        return env


recipe = PyIpfsNodeRecipe()
