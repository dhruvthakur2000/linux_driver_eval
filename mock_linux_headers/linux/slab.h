#pragma once
#define GFP_KERNEL 0
static inline void* kmalloc(int size, int flags) { return 0; }
static inline void kfree(void* ptr) {}
