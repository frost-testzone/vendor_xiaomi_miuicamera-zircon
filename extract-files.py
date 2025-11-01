#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'vendor/xiaomi/miuicamera-zircon',
]


def lib_fixup_system_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'system' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    'vendor.mediatek.hardware.camera.isphal@1.0': lib_fixup_system_suffix,
}

blob_fixups: blob_fixups_user_type = {
    ('system/lib64/libcamera_algoup_jni.xiaomi.so', 'system/lib64/libcamera_mianode_jni.xiaomi.so', 'system/lib64/libcamera_ispinterface_jni.xiaomi.so'): blob_fixup()
        .add_needed('libgui_shim_miuicamera.so'),
    'system/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so', 'android.hardware.graphics.common-V6-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'vendor',
    'xiaomi/miuicamera-zircon',
    device_rel_path='vendor/xiaomi/miuicamera-zircon',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
