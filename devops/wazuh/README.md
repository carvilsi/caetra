# Wazuh Local Testing Environment

This folder contains a Docker Compose setup to run Wazuh locally for testing the Caetra → Wazuh SIEM integration.

## Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Caetra running with `siem_logging_enabled = true` in config
- rsyslog installed on host (to forward Caetra logs to Wazuh) OR journald forwarding configured

### 1. Start Wazuh Manager

```bash
cd devops/wazuh
chmod 644 config/ossec.conf config/local_decoder.xml config/local_rules.xml
docker compose up -d
```

The permissions are required because bind-mounted files must be world-readable for the Wazuh container processes.

Wait 5-10 seconds for the manager to start:

```bash
docker compose ps
# Should show wazuh-manager "Up"
```

### 2. Configure Log Forwarding to Wazuh

Caetra logs JSON events to syslog. Those events need to be forwarded to Wazuh's UDP 514 listener.

**Option A: Using rsyslog (recommended)**

```bash
sudo pacman -S rsyslog
sudo tee /etc/rsyslog.d/49-caetra-siem.conf > /dev/null << 'EOF'
# Forward caetra SIEM logs to local Wazuh manager
:programname, isequal, "caetra_siem" @@127.0.0.1:514
EOF
sudo systemctl restart rsyslog
```

**Option B: Direct UDP (for testing without rsyslog)**

```bash
# Send test event directly to Wazuh
echo '<134>testhost caetra_siem[1]: {"timestamp":"2026-10-01T14:20:00Z","product":"caetra","machine":"test","shield":"usb","state":"triggered","message":"Test event"}' | nc -u localhost 514
```

### 3. Run Caetra and Trigger a Shield

```bash
# In another terminal
cd /path/to/caetra
sudo ./caetra.py
```

Trigger a shield event (e.g., plug in a USB device, toggle backlight, etc.).

### 4. Verify the Alert

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

- **wazuh-manager**: Runs the Wazuh manager. Listens on UDP 514 for syslog events, processes them with decoders/rules, writes alerts to JSON.
- **ossec.conf**: Configured with a syslog listener on UDP 514 (no authentication, for local testing only).
- **local_decoder.xml**: Decodes Caetra's JSON syslog events.
- **local_rules.xml**: Rule 100101 fires when a Caetra shield is triggered.

## Why rsyslog?

Caetra logs JSON to syslog on the host. On Arch Linux:
- Caetra → logs to `/dev/log` (via Python's syslog module)
- journald → receives and stores locally
- **rsyslog** → listens for syslog messages and forwards them over the network to Wazuh UDP 514

Without rsyslog (or another forwarder), logs stay local in journald and never reach Wazuh. Alternatives:
- Configure journald to forward syslog to a network socket
- Modify Caetra to send JSON directly to UDP 514 instead of using syslog

## Configuration Files

- **`ossec.conf`** - Wazuh manager config with syslog listener on UDP 514
- **`local_decoder.xml`** - Decoder for Caetra JSON events
- **`local_rules.xml`** - Rules including rule 100101 for shield events
- **`49-caetra-siem.conf`** - rsyslog config snippet (reference for production)
- **`ossec-agent-snippet.xml`** - Wazuh agent config (reference for production)

## Cleanup

Stop and remove the Wazuh container:

```bash
docker compose down -v
```

The `-v` flag removes the manager's persistent data.

## Notes

- **Testing only**: The syslog listener on UDP 514 is unauthenticated for convenience.
- **Production setup** uses a registered Wazuh agent with authenticated/encrypted communication. See the config files for reference.
- Verified against `wazuh/wazuh-manager:4.14.7`
- Manager API available on port 55000
