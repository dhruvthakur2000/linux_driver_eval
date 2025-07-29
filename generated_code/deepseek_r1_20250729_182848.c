#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "chardev"
#define BUFFER_SIZE 1024  // 1KB buffer

static int major;
static struct cdev cdev;
static char *device_buffer;
static int buffer_offset;
static DEFINE_MUTEX(buffer_mutex);

static int device_open(struct inode *inode, struct file *file)
{
    return 0;
}

static int device_release(struct inode *inode, struct file *file)
{
    return 0;
}

static ssize_t device_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos)
{
    int bytes_to_read;
    int error;

    mutex_lock(&buffer_mutex);
    
    // Calculate available data to read
    bytes_to_read = min(count, (size_t)buffer_offset);
    if (bytes_to_read == 0) {
        mutex_unlock(&buffer_mutex);
        return 0;
    }

    // Copy data to user space
    error = copy_to_user(buf, device_buffer, bytes_to_read);
    if (error) {
        mutex_unlock(&buffer_mutex);
        return -EFAULT;
    }

    // Shift remaining data to beginning of buffer
    memmove(device_buffer, device_buffer + bytes_to_read, BUFFER_SIZE - bytes_to_read);
    buffer_offset -= bytes_to_read;
    
    mutex_unlock(&buffer_mutex);
    return bytes_to_read;
}

static ssize_t device_write(struct file *filp, const char __user *buf, size_t count, loff_t *f_pos)
{
    int free_space;
    int bytes_to_write;
    int error;

    mutex_lock(&buffer_mutex);
    
    // Calculate available space
    free_space = BUFFER_SIZE - buffer_offset;
    if (free_space == 0) {
        mutex_unlock(&buffer_mutex);
        return -ENOSPC;  // No space left
    }

    // Determine how much we can write
    bytes_to_write = min(count, (size_t)free_space);

    // Copy data from user space
    error = copy_from_user(device_buffer + buffer_offset, buf, bytes_to_write);
    if (error) {
        mutex_unlock(&buffer_mutex);
        return -EFAULT;
    }

    buffer_offset += bytes_to_write;
    mutex_unlock(&buffer_mutex);
    return bytes_to_write;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = device_open,
    .release = device_release,
    .read = device_read,
    .write = device_write,
};

static int __init chardev_init(void)
{
    dev_t dev;
    int ret;

    // Allocate buffer
    device_buffer = kmalloc(BUFFER_SIZE, GFP_KERNEL);
    if (!device_buffer)
        return -ENOMEM;

    buffer_offset = 0;

    // Allocate device number
    ret = alloc_chrdev_region(&dev, 0, 1, DEVICE_NAME);
    if (ret < 0) {
        kfree(device_buffer);
        return ret;
    }
    major = MAJOR(dev);

    // Initialize and add character device
    cdev_init(&cdev, &fops);
    cdev.owner = THIS_MODULE;
    ret = cdev_add(&cdev, dev, 1);
    if (ret) {
        unregister_chrdev_region(dev, 1);
        kfree(device_buffer);
        return ret;
    }

    printk(KERN_INFO "chardev: loaded with major %d\n", major);
    return 0;
}

static void __exit chardev_exit(void)
{
    dev_t dev = MKDEV(major, 0);

    cdev_del(&cdev);
    unregister_chrdev_region(dev, 1);
    kfree(device_buffer);

    printk(KERN_INFO "chardev: unloaded\n");
}

module_init(chardev_init);
module_exit(chardev_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("Simple Character Device Driver with 1KB Buffer");


   echo "Test data" > /dev/chardev
   cat /dev/chardev
   