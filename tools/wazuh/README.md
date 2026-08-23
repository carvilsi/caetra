# Wazuh integration

Every shield trigger now also emits a JSON event (timestamp, product,
machine, shield, state, message) to local syslog on facility `local0`
via a dedicated `caetra_siem` logger (`src/utils/logger_setup.py`,
`src/utils/logging_handler.py:log_shield_triggered`). This is in addition
to, not instead of, the existing human-readable log on the `syslog`
facility — nothing about the console/file/Telegram/Canarytokens logging
changes.

Controlled by `[caetra].siem_logging_enabled` in `config/*.toml` (defaults
to `true` if the key is absent). Set it to `false` to stop emitting these
events without touching anything else.

## Try it locally with Docker

`docker-compose.yml` in this folder brings up a single `wazuh-manager`
container (no indexer/dashboard, so results are read from `alerts.json`
rather than a UI) with `local_decoder.xml` and `local_rules.xml` already
installed, and `ossec.conf` opens an extra **unauthenticated** remote
syslog listener on UDP 514 so you can feed it events directly without
enrolling a real agent. This is for trying the feature only — see
"Production setup" below for how a real deployment should look
(agent-based, no open syslog port).

```
cd tools/wazuh
chmod 644 ossec.conf local_decoder.xml local_rules.xml
docker compose up -d
```

`chmod 644` matters: these get bind-mounted with your host user's
ownership, and the manager's `wazuh-analysisd`/`wazuh-remoted` processes
run as a different, unprivileged container user — if the files aren't
world-readable, the manager fails to start with `Error reading XML file
'etc/ossec.conf': (line 0)` (from `ossec.conf` not being readable) or
`Failure to read rule ...` style errors.

Give it 15-20 seconds to finish starting (`docker compose logs -f`, wait
for `Completed.` with no `Configuration error. Exiting` after it), then
run Caetra normally (`sudo ./caetra.py`) with rsyslog forwarding
`local0` to `127.0.0.1:514` (see step 1 under "Production setup" below,
same `49-caetra-siem.conf`, but forward to `127.0.0.1:514` instead of a
remote manager). Trigger a shield and check for the alert:

```
docker exec wazuh-manager grep caetra_shield_triggered /var/ossec/logs/alerts/alerts.json | tail -1
```

You should see a level-10 alert with rule id `100101` and your shield's
message. Tear down with `docker compose down -v` when done (`-v` also
drops the manager's local state/agent keys, fine for a throwaway lab).

This was verified end to end against `wazuh/wazuh-manager:4.14.7`: real
`log_shield_triggered()` output -> rsyslog forwarding -> the manager's
syslog listener -> `local_decoder.xml` (JSON) -> rule `100101` firing
with `$(shield)`/`$(machine)`/`$(message)` correctly interpolated.

## Production setup

On the host running `caetra.py`, with a Wazuh agent installed and
registered:

1. Copy `49-caetra-siem.conf` to `/etc/rsyslog.d/`, `mkdir -p
   /var/log/caetra`, `systemctl restart rsyslog`.
2. Merge the `<localfile>` block from `ossec-agent-snippet.xml` into that
   host's `/var/ossec/etc/ossec.conf`, `systemctl restart wazuh-agent`.

On the Wazuh manager:

3. Copy `local_decoder.xml` to `/var/ossec/etc/decoders/` and
   `local_rules.xml` to `/var/ossec/etc/rules/`.
4. `/var/ossec/bin/wazuh-control restart`.

Trigger a shield (e.g. plug in a USB device) and confirm an alert with
rule id `100101` shows up in Wazuh.

This production path (agent forwards a locally-written file, over the
agent's authenticated/encrypted channel) is deliberately different from
the Docker lab above (raw unauthenticated syslog straight to the
manager) — the lab trades that for not having to enroll an agent just to
try the feature. Do not open the manager's syslog listener like this
outside of a local test.
