#include<linux/input.h>

#include <kernel_additions_headers.h>
#include <lis3lv02d_filter.h>

#define AXES 3

struct movement_t {
        u32 pid;
        u64 ts;
        int axis;
        int value;
        int baseline;
        int delta;
};

BPF_PERF_OUTPUT(events);

// threshold in mg, set from user space; 0 means not configured yet
BPF_ARRAY(threshold, int, 1);
// last known resting position per axis (ABS_X, ABS_Y, ABS_Z)
BPF_HASH(baseline, int, int, AXES);

int movement_observer(struct pt_regs *ctx, struct input_dev *kstrct, unsigned int type, unsigned int code, int value)
{
        if (type != EV_ABS || code > ABS_Z)
                return 0;

        if (!is_lis3lv02d(kstrct))
                return 0;

        int key = 0;
        int *thr = threshold.lookup(&key);
        if (thr == NULL || *thr <= 0)
                return 0;

        int axis = code;
        int *base = baseline.lookup(&axis);
        if (base == NULL) {
                // first sample for this axis, take it as resting position
                baseline.update(&axis, &value);
                return 0;
        }

        int delta = value - *base;
        int abs_delta = delta < 0 ? -delta : delta;
        if (abs_delta <= *thr)
                return 0;

        struct movement_t data = {};

        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();
        data.axis = axis;
        data.value = value;
        data.baseline = *base;
        data.delta = delta;

        // the new position becomes the resting one
        baseline.update(&axis, &value);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
