#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>

#define BUFFER_SIZE 1024

struct my_device {
    struct cdev *cdev;
    unsigned char buffer[BUFFER_SIZE];
    int pos;
};

static int my_device_open(struct cdev *cdev, loff_t *f_pos)
{
    struct my_device *mydev = cdev->private_data;
    mydev->pos = 0;
    return 0;
}

static ssize_t my_device_read(struct file *file, char __user *buf,
                               size_t count, loff_t *f_pos)
{
    struct my_device *mydev = file->private_data;
    ssize_t bytes_read;

    if (mydev->pos >= BUFFER_SIZE) {
        // Buffer is full, return -EIO (end-of-file)
        bytes_read = -EIO;
    } else {
        // Read from buffer
        bytes_read = mydev->pos;
        mydev->pos += bytes_read;

        // Copy data to user space
        if (copy_to_user(buf, mydev->buffer, bytes_read)) {
            // Copy failed, return -EFAULT
            bytes_read = -EFAULT;
        }
    }

    *f_pos = mydev->pos;
    return bytes_read;
}

static ssize_t my_device_write(struct file *file, char __user *buf,
                               size_t count, loff_t *f_pos)
{
    struct my_device *mydev = file->private_data;
    ssize_t bytes_written;

    if (mydev->pos >= BUFFER_SIZE) {
        // Buffer is full, return -EIO (end-of-file)
        bytes_written = -EIO;
    } else {
        // Write to buffer
        bytes_written = mydev->pos;
        mydev->pos += bytes_written;

        // Copy data from user space
        if (copy_from_user(mydev->buffer, buf, bytes_written)) {
            // Copy failed, return -EFAULT
            bytes_written = -EFAULT;
        }
    }

    *f_pos = mydev->pos;
    return bytes_written;
}

static struct file_operations my_device_fops = {
   .owner = THIS_MODULE,
   .read = my_device_read,
   .write = my_device_write,
   .open = my_device_open,
};

static int my_device_probe(struct cdev *cdev, const struct cdev_ops *ops)
{
    struct my_device *mydev;
    int ret;

    mydev = kzalloc(sizeof(struct my_device), GFP_KERNEL);
    if (!mydev) {
        // Allocate failed, return -ENOMEM
        ret = -ENOMEM;
        goto out;
    }

    mydev->cdev = cdev;
    mydev->pos = 0;

    // Register file operations
    if (register_file_ops(cdev->dev, &my_device_fops)) {
        // Registration failed, free memory and return error
        kfree(mydev);
        ret = -EFAULT;
        goto out;
    }

    // Successfully registered file operations
    ret = 0;

out:
    if (ret) {
        // Deregister file operations if an error occurred
        if (cdev->dev) {
            unregister_file_ops(cdev->dev, &my_device_fops);
        }

        // Free memory
        if (mydev) {
            kfree(mydev);
        }
    }

    return ret;
}

module_cdev_driver(my_device_probe, NULL, 0);