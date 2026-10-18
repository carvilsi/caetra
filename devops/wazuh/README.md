# Wazuh Local Testing Environment

This folder contains a Docker Compose setup to run a single-node Wazuh stack
(manager + indexer + dashboard) locally for testing the Caetra → Wazuh SIEM
integration. It is based on the official
[wazuh-docker `single-node`](https://github.com/wazuh/wazuh-docker/tree/v4.14.7/single-node)
deployment, plus Caetra's syslog listener, decoder and rules.

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Caetra running with `siem_logging_enabled = true` in config (and
  `siem_host`/`siem_port` pointing at the manager; defaults to `127.0.0.1:514`)

### 1. Generate the TLS certificates (first time only)

The indexer, manager (Filebeat) and dashboard talk to each other over TLS:

```bash
cd devops/wazuh
docker compose -f generate-indexer-certs.yml run --rm generator
```

This writes the certificates to `config/wazuh_indexer_ssl_certs/` (gitignored),
owned by the containers' UIDs, so you can't read them as your own user. A
`find: command not found` line in the output is harmless.

### 2. Start Wazuh

```bash
docker compose up -d
docker compose ps
```

Give it a minute or two: the indexer initializes its security index on first
start, and the manager waits for it.

- Dashboard: **https://localhost** (self-signed cert)
- Indexer: `https://localhost:9200`
- Manager API: `https://localhost:55000`

### Default credentials

These are the wazuh-docker demo defaults (test lab only):

| Service | Username | Password | Used for |
|---|---|---|---|
| Dashboard / Indexer | `admin` | `SecretPassword` | Logging in at https://localhost; indexer API at `:9200` (also used by the manager's Filebeat) |
| Indexer | `kibanaserver` | `kibanaserver` | Internal account the dashboard uses to talk to the indexer |
| Manager API | `wazuh-wui` | `MyS3cr37P450r.*-` | Wazuh API at `:55000` (also used by the dashboard) |

They're set in `docker-compose.yml` (`INDEXER_PASSWORD`, `DASHBOARD_PASSWORD`,
`API_PASSWORD`), `config/wazuh_dashboard/wazuh.yml` and, as hashes,
`config/wazuh_indexer/internal_users.yml`. Changing an indexer password
means updating the hash in `internal_users.yml` too, not just the compose env.

### 3. Check the Decoder (optional)

Caetra sends each shield event as a plain UDP datagram straight to the
manager's published UDP 514 port — no forwarder (socat/rsyslog) is needed:

```
caetra_siem: {"timestamp": "...", "product": "caetra", "machine": "...", "shield": "...", "state": "triggered", "message": "..."}
```

Check the decoder and rule against a sample line:

```bash
echo 'caetra_siem: {"product":"caetra","machine":"test","shield":"usb","state":"triggered","message":"Test event"}' \
  | docker exec -i wazuh-manager /var/ossec/bin/wazuh-logtest
```

It should decode as `caetra-siem` and match rule `100101`. To push the same
line through remoted end to end:

```bash
echo 'caetra_siem: {"product":"caetra","machine":"test","shield":"usb","state":"triggered","message":"Test event"}' | nc -u -w1 localhost 514
```

### 4. Run Caetra and Trigger a Shield

```bash
# In another terminal
cd /path/to/caetra
sudo ./caetra.py
```

Trigger a shield event (e.g., plug in a USB device, toggle backlight, etc.).

### 5. Verify the Alert

Check Wazuh received the alert:

```bash
docker exec wazuh-manager tail -f /var/ossec/logs/alerts/alerts.json | jq .
```

Filter for Caetra events:

```bash
docker exec wazuh-manager grep caetra_shield_triggered /var/ossec/logs/alerts/alerts.json | tail -1 | jq .
```

You should see a level-10 alert with rule ID `100101` and your shield's message.

## Architecture

- **wazuh-manager**: Listens on UDP 514 for syslog events, processes them with decoders/rules, writes alerts to `alerts.json`, and ships them to the indexer via Filebeat.
- **wazuh-indexer**: OpenSearch-based store for alerts.
- **wazuh-dashboard**: Web UI on https://localhost.

The manager's config files (`ossec.conf`, `local_decoder.xml`,
`local_rules.xml`) are mounted under `/wazuh-config-mount`, which the image's
init copies into `/var/ossec`. To apply edits, recreate the container (volumes
are kept):

```bash
docker compose up -d --force-recreate wazuh.manager
```

Don't use `docker compose restart`: on a restart the 4.14.7 image's init fails
re-seeding `/var/ossec/var/multigroups` (`Error executing command: 'cp -ar
.../multigroups/. ...'`) and skips the config copy, so the manager keeps
running with the old files.

## How events reach Wazuh

Caetra's `caetra_siem` logger uses a small UDP handler
(`src/utils/logger_setup.py`) that sends `caetra_siem: {json}` to
`siem_host:siem_port`. Docker publishes the manager's UDP 514 on the host, so
with the defaults events go straight from Caetra to remoted. To ship to a
remote manager, set `siem_host` to its address.

## Configuration Files

- **`config/ossec.conf`** - official single-node manager config plus the syslog listener on UDP 514
- **`config/local_decoder.xml`** - Decoder for Caetra JSON events
- **`config/local_rules.xml`** - Rules including rule 100101 for shield events
- **`config/certs.yml`**, **`generate-indexer-certs.yml`** - certificate generation
- **`config/wazuh_indexer/`**, **`config/wazuh_dashboard/`** - official indexer/dashboard config (demo users and passwords)

## Cleanup

Stop and remove the Wazuh containers:

```bash
docker compose down -v
```

The `-v` flag removes the manager's and indexer's persistent data. The
generated certificates in `config/wazuh_indexer_ssl_certs/` are kept.

## Troubleshooting

**No alerts appearing in Wazuh:**
- Verify Caetra is sending: `sudo tcpdump -i lo -A udp port 514`
- Verify `siem_logging_enabled = true` and `siem_host`/`siem_port` in Caetra's config
- Check Wazuh is receiving events: `docker compose logs wazuh.manager | grep -i syslog`
- Test the decoder with `wazuh-logtest` (see step 3)

## Notes

- **Testing only**: The syslog listener on UDP 514 is unauthenticated for convenience.
- **Production setup** uses a registered Wazuh agent with authenticated/encrypted communication. See the config files for reference.
- **Demo credentials**: see [Default credentials](#default-credentials); don't reuse this setup outside a local test lab.
- Verified against Wazuh `4.14.7`
