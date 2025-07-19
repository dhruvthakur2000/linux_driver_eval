#ifndef _LINUX_FS_H
#define _LINUX_FS_H

struct file {
    void *private_data;
};

struct cdev {
    void *private_data;
};

#endif
