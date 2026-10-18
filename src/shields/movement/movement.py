import ctypes as ct
import glob

from src.shields.shields_common import (
    os,
    constants,
    deploying,
    logger_shields,
    log_shield_exception,
    log_shield_triggered,
    log_shield_exception_warn,
    send,
    status_handler,
    ConfigurationError,
    MaxActionReached,
    ShieldConfigurationError,
)

# shield name
# must be same with in toml root config
SHIELD_NAME = "movement"

# kernel section

# kprobe event name
event = "input_handle_event"
# c function for the kprobe
fn_name = "movement_observer"
# c source file; the name must be the same that the Shield name
src_file = SHIELD_NAME + ".c"

# input device name registered by lis3lv02d driver
ACCELEROMETER_NAME = "ST LIS3LV02DL Accelerometer"
AXES = ("x", "y", "z")

status = status_handler.StatusHandler()


# the lis3lv02d driver only polls the sensor while its input device is open,
# so we keep it open for the whole life of the shield
def open_accelerometer():
    for name_file in glob.glob("/sys/class/input/event*/device/name"):
        with open(name_file) as f:
            if f.read().strip() == ACCELEROMETER_NAME:
                event_dev = name_file.split("/")[4]
                return os.open(f"/dev/input/{event_dev}", os.O_RDONLY | os.O_NONBLOCK)

    message = f"no '{ACCELEROMETER_NAME}' input device found; check that lis3lv02d driver is loaded"
    raise ShieldConfigurationError(message)


def bpf_main():
    try:
        # shield configuration
        config = deploying.load_shield_config(SHIELD_NAME)
        shield_config = config.get(SHIELD_NAME)

        if shield_config.get("enable"):
            # BPF object
            b = deploying.load_bpf_prog(
                SHIELD_NAME,
                event,
                fn_name,
                src_file,
                shield_config.get("description"),
                shield_config.get("features"),
            )

            b["threshold"][ct.c_int(0)] = ct.c_int(
                shield_config["features"]["threshold"]
            )
            accelerometer_fd = open_accelerometer()  # noqa: F841

            # Write here the logic for your shield
            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                # get here the data for shield impl
                movement_data = "axis:%s-value:%d-baseline:%d-delta:%d-pid:%d" % (
                    AXES[event.axis],
                    event.value,
                    event.baseline,
                    event.delta,
                    event.pid,
                )

                message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get('action_label')}' limit_sending: {shield_config['features']['limit_sending']} data: {movement_data}"
                try:
                    if shield_config["features"]["limit_sending"]:
                        status.can_be_sent(
                            event.ts,
                            shield_config["features"]["max_actions"],
                            shield_config["features"]["cool_down_time"],
                        )

                    send(message, shield_config)
                except ConfigurationError as e:
                    log_shield_exception(e, SHIELD_NAME)
                except KeyboardInterrupt:
                    exit()
                except MaxActionReached as e:
                    log_shield_exception_warn(e, SHIELD_NAME)
                else:
                    logger_shields.info(f"{SHIELD_NAME} triggered and sent: {message}")
                finally:
                    log_shield_triggered(SHIELD_NAME, message)

            b["events"].open_perf_buffer(shield_logic)
            while 1:
                try:
                    b.perf_buffer_poll()
                except ValueError:
                    continue
                except KeyboardInterrupt:
                    exit()
        else:
            logger_shields.warning("[-] " + SHIELD_NAME.upper() + " Shield disabled.")

    except ShieldConfigurationError as e:
        log_shield_exception(e, SHIELD_NAME)
    except Exception as e:
        log_shield_exception(e, SHIELD_NAME)


if __name__ == "__main__":
    bpf_main()
