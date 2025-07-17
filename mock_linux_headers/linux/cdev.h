#pragma once
struct cdev { int dummy; };
static inline int cdev_register(void *c) { return 0; }
static inline void cdev_unregister(void *c) {}
