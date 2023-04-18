#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
# Download and build the data if it does not exist.

import parlai.core.build_data as build_data
import os
from parlai.core.build_data import DownloadableFile
from parlai.utils.io import PathManager

RESOURCES = [
    DownloadableFile(
        "0BwmD_VLjROrfN0xhTDVteGQ3eG8",
        "qadailymail.tar.gz",
        "77bfe0d91dbc9774991bbce59895743adfc984eafffc328a7b1d34a89e2b5646",
        from_google=True,
    )
]


def _process(fname, fout):
    with PathManager.open(fname) as f:
        lines = [line.strip("\n") for line in f]
    # main article
    s = "1 " + lines[2]
    # add question
    s = s + " " + lines[4]
    # add answer
    s = s + "\t" + lines[6]
    # add candidates (and strip them of the real names)
    for i in range(8, len(lines)):
        lines[i] = lines[i].split(":")[0]
    s = s + "\t\t" + "|".join(lines[8:])
    fout.write(s + "\n\n")


def create_fb_format(outpath, dtype, inpath):
    print("building fbformat:" + dtype)
    with PathManager.open(os.path.join(outpath, dtype + ".txt"), "w") as fout:
        for f in os.listdir(inpath):
            if f.endswith(".question"):
                fname = os.path.join(inpath, f)
                _process(fname, fout)


def build(opt):
    version = "v1.0"
    dpath = os.path.join(opt["datapath"], "QADailyMail")

    if not build_data.built(dpath, version):
        print("[building data: " + dpath + "]")
        if build_data.built(dpath):
            # An older version exists, so remove these outdated files.
            build_data.remove_dir(dpath)
        build_data.make_dir(dpath)

        # Download the data.
        for downloadable_file in RESOURCES:
            downloadable_file.download_file(dpath)

        ext = os.path.join("dailymail", "questions")
        create_fb_format(dpath, "train", os.path.join(dpath, ext, "training"))
        create_fb_format(dpath, "valid", os.path.join(dpath, ext, "validation"))
        create_fb_format(dpath, "test", os.path.join(dpath, ext, "test"))

        # Mark the data as built.
        build_data.mark_done(dpath, version)
