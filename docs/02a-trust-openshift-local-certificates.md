# 02a — Trust OpenShift Local certificates

**Estimated time: 5–10 minutes**

After OpenShift Local is running, routes under `*.apps-crc.testing` (including the web console **and the image registry**) use TLS certificates signed by a **cluster-local root CA**. Browsers and tools on your laptop do **not** trust that CA by default, so you see warnings or TLS errors.

This page shows how to export the Ingress root CA and import it into your workstation trust store.

> For **local development only**. Do not install this CA on production or shared corporate machines.

## Prerequisites

```bash
crc status          # cluster should be Running
oc whoami           # logged in (kubeadmin or developer)
```

## 1. Export the root CA

### Linux / macOS

Preferred (from the cluster secret):

```bash
oc get secret router-ca -n openshift-ingress-operator \
  -o jsonpath='{.data.tls\.crt}' | base64 -d > crc-root-ca.pem
```

Alternative (from the console TLS handshake):

```bash
openssl s_client -showcerts -verify 5 \
  -connect console-openshift-console.apps-crc.testing:443 </dev/null 2>/dev/null \
  | openssl x509 -out crc-root-ca.pem
```

Verify it looks like a self-signed root (subject ≈ issuer):

```bash
openssl x509 -in crc-root-ca.pem -noout -subject -issuer
```

### Windows (PowerShell)

```powershell
# Ensure oc is on PATH (from crc oc-env / OpenShift Local install)
$b64 = oc get secret router-ca -n openshift-ingress-operator -o jsonpath="{.data.tls\.crt}"
[IO.File]::WriteAllBytes(
  "$PWD\crc-root-ca.pem",
  [Convert]::FromBase64String($b64)
)
```

Optional check if OpenSSL is installed:

```powershell
openssl x509 -in crc-root-ca.pem -noout -subject -issuer
```

## 2. Import into the OS trust store

### Linux — RHEL / Fedora / CentOS Stream

```bash
sudo cp crc-root-ca.pem /etc/pki/ca-trust/source/anchors/crc-root-ca.pem
sudo update-ca-trust
```

### Linux — Debian / Ubuntu

`update-ca-certificates` expects a `.crt` file:

```bash
sudo cp crc-root-ca.pem /usr/local/share/ca-certificates/crc-root-ca.crt
sudo update-ca-certificates
```

### Windows — PowerShell (recommended)

**Current user** (no admin required in many setups):

```powershell
Import-Certificate -FilePath .\crc-root-ca.pem -CertStoreLocation Cert:\CurrentUser\Root
```

**Local machine** (run PowerShell as Administrator):

```powershell
Import-Certificate -FilePath .\crc-root-ca.pem -CertStoreLocation Cert:\LocalMachine\Root
```

Or with `certutil` (Administrator):

```powershell
certutil -addstore -f ROOT .\crc-root-ca.pem
```

GUI alternative: open `certlm.msc` → **Trusted Root Certification Authorities** → **Certificates** → **All Tasks** → **Import** → select `crc-root-ca.pem`.

### macOS (optional)

```bash
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain crc-root-ca.pem
```

## 3. Restart clients and verify

Restart browsers and any long-running tools (`curl`, IDEs, Postman) so they reload the trust store.

```bash
# Linux / macOS — should not report certificate verify failures
curl -vI https://console-openshift-console.apps-crc.testing 2>&1 | grep -iE 'SSL certificate verify|issuer:|subject:'
```

**Windows (`curl.exe` + Schannel):** after the CA is trusted, revocation checks can still fail for a local CA. Use:

```powershell
curl.exe --ssl-no-revoke -I https://console-openshift-console.apps-crc.testing
# Expect: HTTP/1.1 200
```

Open https://console-openshift-console.apps-crc.testing — the untrusted-certificate interstitial should be gone (or reduced to a normal login).

### Notes

- **Firefox** may use its own certificate store; import the PEM there if the system store is ignored.
- If you recreate the OpenShift Local cluster (`crc delete` / new start), export and re-import the CA again — the Ingress CA can change.
- Java / Jib clients sometimes need insecure registry mode for the CRC registry route (`-Dquarkus.container-image.insecure=true`) even after trusting the CA — chapter 04 uses that flag.
- On Windows, `Import-Certificate` into **Trusted Root** shows a Security Warning — click **Yes** to finish.
- Do **not** commit `crc-root-ca.pem` (it is listed in `.gitignore`).

## Next

→ [03 — Joke operator project](./03-scaffold-joke-operator.md)
