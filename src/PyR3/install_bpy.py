# -*- coding: utf-8 -*-
import os
import platform
import shutil
import site
import subprocess
import tarfile
from pathlib import Path

import requests

IS_LINUX = platform.system() == "Linux"
IS_WINDOWS = platform.system() == "Windows"

BPY_WIN_DIST_NAME = "bpy_2_93-win_amd64-cp39.tar.gz"
BPY_LINUX_DIST_NAME = "bpy_2_93-linux_64-cp39.tar.gz"


def install_bpy_lib():
    if check_unpack_required():
        if IS_WINDOWS:
            unpack_windows()
        elif IS_LINUX:
            unpack_linux()
            subprocess.Popen(["sudo", "apt", "install", "libpulse0"]).wait()
        else:
            raise RuntimeError(
                "This operating system is not supported. We support only Windows and Linux."
            )


def unpack_linux():
    tarfile_path = bpy_tar_gz_path()
    with tarfile.open(tarfile_path) as archive:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(archive, get_site_packages_dir(), members=archive.getmembers())
            get_site_packages_dir(), members=archive.getmembers()
        )
    os.remove(tarfile_path)


def unpack_windows():
    tarfile_path = bpy_tar_gz_path()
    with tarfile.open(tarfile_path) as archive:
        folder_2_93_members = [
            member
            for member in archive.getmembers()
            if member.path.startswith("./2.93/")
        ]
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(archive, get_python_executable_dir(), members=folder_2_93_members)
            get_python_executable_dir(), members=folder_2_93_members
        )
        other_members = [
            member
            for member in archive.getmembers()
            if not member.path.startswith("./2.93/")
        ]
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(archive, get_site_packages_dir(), members=other_members)
    os.remove(tarfile_path)


def check_unpack_required():
    try:
        import bpy

        bpy.__name__
    except ImportError:
        return True
    return False


def is_installed():
    end_path = os.path.join("src", "PyR3", "unpack.py")
    if Path(__file__).__str__().endswith(end_path):
        return False
    return True


def get_python_executable_dir() -> Path:
    return Path(os.__file__).parent.parent


def get_site_packages_dir() -> Path:
    for path in site.getsitepackages():
        if "site-packages" in path:
            return Path(path)


if is_installed():

    def bpy_tar_gz_path() -> Path:
        lib_dir = Path(__file__).parent.parent.parent
        if IS_WINDOWS:
            path = lib_dir / BPY_WIN_DIST_NAME
            if not os.path.exists(path):
                download_bpy_binaries(
                    BPY_WIN_DIST_NAME,
                    path,
                )
        elif IS_LINUX:
            path = lib_dir / BPY_LINUX_DIST_NAME
            if not os.path.exists(path):
                download_bpy_binaries(
                    BPY_LINUX_DIST_NAME,
                    path,
                )
        return path


else:

    def bpy_tar_gz_path() -> Path:
        if IS_WINDOWS:
            path = (
                Path(__file__).parent.parent.parent
                / "lib"
                / "win"
                / BPY_WIN_DIST_NAME
            )
            if not os.path.exists(path):
                download_bpy_binaries(
                    BPY_WIN_DIST_NAME,
                    path,
                )
        elif IS_LINUX:
            path = (
                Path(__file__).parent.parent.parent
                / "lib"
                / "linux"
                / BPY_LINUX_DIST_NAME
            )
            if not os.path.exists(path):
                download_bpy_binaries(
                    BPY_LINUX_DIST_NAME,
                    path,
                )
        return path


def download_bpy_binaries(dist: str, local_path: Path):
    download_file(
        f"https://github.com/Argmaster/pyr3/releases/download/bpy-binaries/{dist}",
        local_path,
    )


def download_file(url: str, local_path: Path):
    local_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def get_path_members(archive: tarfile.TarFile, path: str):
    return [
        member
        for member in archive.getmembers()
        if member.path.startswith(path)
    ]


if __name__ == "__main__":
    install_bpy_lib()
