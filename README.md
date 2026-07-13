# SCIDROW HUNTER v2.3.4 — Autonomous Behavioral Threat Interceptor

Stop wasting your RAM on corporate antivirus bloatware.

### How it works:
1. **Zero-Signature Behavioral Analysis:** It doesn't look for known malware hashes. It monitors the behavior of running processes on the hardware level.
2. **Multi-Threaded Customs Officer:** Inspects all active LISTEN/ESTABLISHED network connections every 5 seconds in a background thread.
3. **Parent PID Validation:** Traces process lineage back to its roots. If a system process (like smartscreen.exe) is spawned by an unverified binary inside Temp/AppData/Downloads, it nukes the entire branch immediately to prevent process hollowing.
4. **Cryptographic Caching:** Dynamically verifies binary integrity via SHA-256 to stop whitelist name-spoofing.
5. **DPAPI & Tdata Interception:** Monitors unauthorized file descriptor access targeting Chrome's "Login Data" and Telegram's session paths.
6. **Anti-Sleep Countermeasure:** Catches delayed-execution malware by analyzing zeroed CPU execution runtimes.


### How to deployment:
* **For Professionals (.py):** Review the clean, fully transparent Python source code in Notepad. No hidden backdoors. Requires `pip install psutil`.
* **For Casual Users (.exe):** Download the standalone pre-compiled executable from the Releases page—no Python installation required.

---
### Support the project:
This tool is 100% free and open-source. If Scidrow Hunter saved your production server or protected your company's database, consider buying a cup of coffee for the independent developer. 

* **USDT (TRC-20) Wallet Address:** TEWQScWrBB2B4brjWL5nfxrWzNwitTuD6i

