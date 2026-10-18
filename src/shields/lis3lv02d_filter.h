// helper to recognize the ST lis3lv02d accelerometer (e.g. Dell Latitude
// freefall/accelerometer sensor) on input subsystem kprobes.
// the driver registers the input device with phys "lis3lv02d/input0"
#ifndef LIS3LV02D_FILTER_H
#define LIS3LV02D_FILTER_H

#define LIS3LV02D_PHYS_PREFIX "lis3lv02d"
#define LIS3LV02D_PHYS_PREFIX_LEN (sizeof(LIS3LV02D_PHYS_PREFIX) - 1)

static __always_inline int is_lis3lv02d(struct input_dev *dev)
{
        const char prefix[] = LIS3LV02D_PHYS_PREFIX;
        char phys[LIS3LV02D_PHYS_PREFIX_LEN + 1] = {};
        const char *phys_ptr = NULL;

        // read the pointer explicitly, phys can be NULL for some devices
        bpf_probe_read_kernel(&phys_ptr, sizeof(phys_ptr), &dev->phys);
        if (phys_ptr == NULL)
                return 0;

        bpf_probe_read_kernel_str(phys, sizeof(phys), phys_ptr);

        #pragma unroll
        for (int i = 0; i < LIS3LV02D_PHYS_PREFIX_LEN; i++) {
                if (phys[i] != prefix[i])
                        return 0;
        }

        return 1;
}

#endif // LIS3LV02D_FILTER_H
