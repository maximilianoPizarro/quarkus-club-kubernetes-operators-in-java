# 01 — Prerequisites

Before you start the 101 path, install the tools below. You need a machine that can run a local OpenShift cluster (laptop or desktop).

## Account

1. Create a free [Red Hat Developer](https://developers.redhat.com/) account (no paid subscription required for OpenShift Local).
2. Accept the developer program terms so you can download OpenShift Local / pull related images.

## Runtime stack

| Tool | Why |
|------|-----|
| [Podman Desktop](https://podman-desktop.io/) | Local containers + OpenShift Local extension |
| [OpenShift Local](https://developers.redhat.com/products/openshift-local) | Single-node OpenShift on your laptop (Console + OLM) |
| `oc` | OpenShift CLI (often installed with OpenShift Local) |
| [operator-sdk](https://sdk.operatorframework.io/docs/installation/) | Validate and run OLM bundles |
| JDK 17+ and Maven | Build Quarkus / QOSDK projects |
| [Quarkus CLI](https://quarkus.io/guides/cli-tooling) (optional) | Scaffold operator projects quickly |

## Platform notes

- **Linux (RHEL / Fedora):** natural fit for Podman and OpenShift Local.
- **Windows / macOS:** supported by OpenShift Local; follow the official install guide for hypervisor requirements (Hyper-V, HyperKit, etc.).
- Give the VM enough resources (OpenShift Local docs recommend generous CPU/RAM — typically 4+ CPUs and 8+ GB RAM for a usable Console).

## Verify CLIs

```bash
podman --version
oc version --client
operator-sdk version
java -version
mvn -version
```

Optional:

```bash
quarkus --version
```

## Prefer pure Kubernetes?

OpenShift Local is the path this tutorial uses so you get **OperatorHub / OLM** and the **OpenShift Console**. If you prefer not to use a Red Hat login, you can run operators on **kind** with `operator-sdk run bundle`, but you will not get the same Console experience. See the short note in [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md).

## Next

→ [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md)

After the cluster is up, trust the Ingress CA: [02a — Trust OpenShift Local certificates](./02a-trust-openshift-local-certificates.md).
