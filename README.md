# SCIDROW HUNTER v2.3.4 — Lightweight Endpoint Telemetry & Core Directory Integrity Guard

A standalone, zero-signature local host monitor designed for low-overhead security auditing and proactive process lineage verification under Windows environments.

Stop wasting your RAM on corporate endpoint telemetry and background bloatware overhead.

### How it works:

1. **Zero-Signature Behavioral Analysis:** The tool does not rely on static signature databases or cloud lookups. It continuously audits running process activities directly at the hardware-host interface level.
2. **Multi-Threaded Socket Auditor:** A dedicated background thread executes every 5 seconds, inspecting all active LISTEN and ESTABLISHED network connections.
3. **Parent PID Validation:** Traces active network-socket ownership back to its architectural origin. If a protected Windows system binary (e.g., smartscreen.exe) or an unverified module is spawned from temporary user paths (Temp/AppData/Downloads), the monitor intervenes and terminates the entire process tree to mitigate unauthorized hollowing patterns.
4. **Cryptographic Integrity Layer:** Dynamically caches verified process identity indicators (SHA-256 hashes) in volatile memory to eliminate local whitelist name-spoofing and masquerading tactics.
5. **Data Isolation Auditing:** Constantly monitors active file descriptors. It flags unverified applications attempting to open, lock, or read secure local data stores (including web-browser login state profiles and instant messenger session data) while simultaneously maintaining an active internet socket.
6. **Execution Metric Checking:** Analyzes thread runtime execution metrics to detect anomalies from delayed-execution background elements trying to idle in physical memory.

### How to deployment:

* **For Professionals (.py):** Review the transparent Python source code in any local text editor. Requires no hidden dependencies except `pip install psutil`.
* **Standalone Deployment:** Fully compatible with direct script execution and custom local automation deployments under standalone environments.

---

### Support the project:

This tool is 100% free, telemetry-free, and open-source. If Scidrow Hunter protected your local environment or optimized your server resources, consider supporting independent development.

* **USDT (TRC-20) Wallet Address:** `TEWQScWrBB2B4brjWL5nfxrWzNwitTuD6i`
