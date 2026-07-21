# 02 — Podman Desktop & OpenShift Local

**Estimated time: 20–30 minutes** (first `crc start` can take longer)

Goal: a local OpenShift cluster with OLM, Console, and an **internal image registry**, ready for the Joke operator.

Official product page: [Red Hat OpenShift Local](https://developers.redhat.com/products/openshift-local) (formerly CodeReady Containers).

## Install Podman Desktop

1. Download and install [Podman Desktop](https://podman-desktop.io/).
2. Complete the first-run setup so Podman can create machines / run containers on your OS.

> Podman is useful, but this tutorial’s default path builds/pushes the **operator image with Jib** and the **bundle image with an OpenShift Build** — so a working cluster registry matters more than a local Podman machine.

## Install OpenShift Local

1. In Podman Desktop, open the **Extensions** (or **Catalog**) view and install the **OpenShift Local** / CRC-related extension if prompted.
2. Or follow the download and CLI install steps from [developers.redhat.com/products/openshift-local](https://developers.redhat.com/products/openshift-local).
3. Sign in with your free Red Hat Developer account when asked for pull secrets / credentials.

Typical CLI flow (names may vary slightly by version):

```bash
# After installing the crc / OpenShift Local binary on your PATH:
crc setup
crc start
```

When `crc start` finishes, it prints login commands. Example pattern:

```bash
eval $(crc oc-env)   # Linux/macOS — puts oc on PATH for this shell
oc login -u kubeadmin -p <password> https://api.crc.testing:6443
```

On Windows, use the `oc` path and login command printed by OpenShift Local / CRC (or `crc console --credentials`).

## Verify the cluster

```bash
oc whoami
oc get nodes
oc get csv -A | head
oc registry info
```

`oc registry info` should print something like:

```text
default-route-openshift-image-registry.apps-crc.testing
```

That host is the **external** push/pull URL for the OpenShift Local registry. Inside the cluster, pods pull via:

```text
image-registry.openshift-image-registry.svc:5000
```

Open the OpenShift Console URL from `crc console` (or the Podman Desktop OpenShift Local UI). Confirm you can browse **Operators → OperatorHub**.

## Kind alternative (optional)

If you skip OpenShift Local and use **kind**:

- You can still build and run many operators with `operator-sdk run bundle`.
- You will **not** get the OpenShift Console / OperatorHub UX used in the Quarkus Club slides.
- You will need another registry (or `kind load`) instead of the OpenShift Local registry used in chapters 04–05.

## Next

→ [02a — Trust OpenShift Local certificates](./02a-trust-openshift-local-certificates.md) (recommended after install)

→ [03 — Joke operator project](./03-scaffold-joke-operator.md)
