import os

MOCK_DIR = "mock_linux_headers/linux"
os.makedirs(MOCK_DIR, exist_ok=True)

mock_headers = {
    "module.h": """#pragma once
#define THIS_MODULE 0
""",

    "fs.h": """#pragma once
struct file { int dummy; };
struct inode { int dummy; };
""",

    "cdev.h": """#pragma once
struct cdev { int dummy; };
static inline int cdev_register(void *c) { return 0; }
static inline void cdev_unregister(void *c) {}
""",

    "uaccess.h": """#pragma once
#define __user
""",

    "init.h": """#pragma once
#define module_init(x)
#define module_exit(x)
""",

    "slab.h": """#pragma once
#define GFP_KERNEL 0
static inline void* kmalloc(int size, int flags) { return 0; }
static inline void kfree(void* ptr) {}
""",

    "device.h": """#pragma once
""",

    "types.h": """#pragma once
#define NULL 0
typedef unsigned long size_t;
typedef long ssize_t;
"""
}

for filename, content in mock_headers.items():
    path = os.path.join(MOCK_DIR, filename)
    with open(path, "w") as f:
        f.write(content)

print(" Mock Linux kernel headers generated in 'mock_linux_headers/linux/'")
