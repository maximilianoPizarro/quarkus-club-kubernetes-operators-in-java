# 01 — Prerequisites

**Estimated time: 15–20 minutes** (skip if the tools are already installed)

Before you start the 101 path, install the tools below. You need a machine that can run a local OpenShift cluster (laptop or desktop).

## Account

1. Create a free [Red Hat Developer](https://developers.redhat.com/) account (no paid subscription required for OpenShift Local).
2. Accept the developer program terms so you can download OpenShift Local / pull related images.

## Runtime stack

| Tool | Why |
|------|-----|
| [Podman Desktop](https://podman-desktop.io/) | Local containers + OpenShift Local extension |
| [OpenShift Local](https://developers.redhat.com/products/openshift-local) | Single-node OpenShift on your laptop (Console + OLM + **internal image registry**) |
| `oc` | OpenShift CLI (often installed with OpenShift Local) |
| [operator-sdk](https://sdk.operatorframework.io/docs/installation/) | Validate bundles and `run bundle` (Linux binary; on Windows run it inside the CRC VM — see [05](./05-deploy-and-verify.md)) |
| JDK 17+ (21 recommended) and Maven | Build Quarkus / QOSDK projects |
| [Quarkus CLI](https://quarkus.io/guides/cli-tooling) | Scaffold the operator project (`quarkus create app`) |

This tutorial uses the **OpenShift Local internal registry** (no Quay / Docker Hub account required for the 101 path).

## Platform notes

- **Linux (RHEL / Fedora):** natural fit for Podman and OpenShift Local.
- **Windows / macOS:** supported by OpenShift Local; follow the official install guide for hypervisor requirements (Hyper-V, HyperKit, etc.).
- Give the VM enough resources (OpenShift Local docs recommend generous CPU/RAM — typically 4+ CPUs and 8+ GB RAM for a usable Console).
- **Windows tip:** if the `oc` shipped under `%USERPROFILE%\.crc\bin\oc` requires elevation, use the `oc` that CRC/`oc` installers put on your PATH (for example under `Program Files (x86)\oc`).

## Verify CLIs

```bash
podman --version          # optional for this path (bundle can be built in-cluster)
oc version --client
operator-sdk version      # Linux/macOS, or WSL on Windows
java -version
mvn -version
quarkus --version
```

Install Quarkus CLI (user-local, via JBang) if needed:

```bash
curl -Ls https://sh.jbang.dev | bash -s - app setup
# new shell, then:
jbang app install quarkus@quarkusio
quarkus --version
```

## Prefer pure Kubernetes?

OpenShift Local is the path this tutorial uses so you get **OperatorHub / OLM**, the **OpenShift Console**, and a local **image registry**. If you prefer not to use a Red Hat login, you can run operators on **kind** with `operator-sdk run bundle`, but you will not get the same Console experience. See the short note in [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md).

## Next

→ [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md)

After the cluster is up, trust the Ingress CA: [02a — Trust OpenShift Local certificates](./02a-trust-openshift-local-certificates.md).
