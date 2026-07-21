# Quarkus Club — Kubernetes Operators in Java

Hands-on tutorial and presentation slides for the Quarkus Club session on building Kubernetes operators with **Quarkus** and the **Java Operator SDK (JOSDK)** / **Quarkus Operator SDK (QOSDK)**.

This repository walks you from installing **Podman Desktop** and **[OpenShift Local](https://developers.redhat.com/products/openshift-local)** through deploying a simple **Joke** operator — a 101 path anyone can reproduce with a free [Red Hat Developer](https://developers.redhat.com/) account.

Images are built and stored in the **OpenShift Local internal registry** (no Quay account required for the lab).

The ready-to-run operator lives in [`joke-operator/`](./joke-operator/) (based on the Quarkiverse Joke sample, with workshop fixes already applied).

> **Slides only** — speaker scripts are not included in this repository.

## Live slides (talk day)

After GitHub Pages is enabled:

**https://maximilianopizarro.github.io/quarkus-club-kubernetes-operators-in-java/**

- Open in a browser · use arrow keys to navigate
- PDF download: [slides/quarkus-club-operators.pdf](./slides/quarkus-club-operators.pdf)

### Enable GitHub Pages (one-time)

1. Repo **Settings** → **Pages**
2. **Source**: GitHub Actions
3. Push to `main` (or re-run the **Deploy GitHub Pages** workflow)

## Mandatory path (do these in order)

Do **not** skip steps marked mandatory. Optional steps are labeled as such in each doc.

| Order | Module | Mandatory? | What you must finish before continuing |
|------:|--------|:----------:|----------------------------------------|
| 1 | [Prerequisites](./docs/01-prerequisites.md) | **Yes** | JDK 21, Maven/Quarkus CLI, `oc`, `operator-sdk`, Podman Desktop installed |
| 2 | [Podman Desktop & OpenShift Local](./docs/02-podman-desktop-openshift-local.md) | **Yes** | `crc start` done; `oc login` as kubeadmin works |
| 2a | [Trust OpenShift Local certificates](./docs/02a-trust-openshift-local-certificates.md) | **Yes** (once per machine) | Browser/CLI trust the CRC Ingress CA |
| 3 | [Joke operator project](./docs/03-scaffold-joke-operator.md) | **Yes** | Use the committed `joke-operator/` tree (no clone required) |
| 4 | [Build against the OpenShift Local registry](./docs/04-build-bundle-operator-sdk.md) | **Yes** | Operator image **and** bundle image both present in the registry |
| 5 | [Deploy and verify](./docs/05-deploy-and-verify.md) | **Yes** | CSV `Succeeded`, pod Running, JokeRequest reconciles |

**Total hands-on:** ~90–120 min.

### Quick restart (cluster already set up)

If OpenShift Local is already running and trusted, start here:

```bash
git clone https://github.com/maximilianoPizarro/quarkus-club-kubernetes-operators-in-java.git
cd quarkus-club-kubernetes-operators-in-java/joke-operator
# then follow docs/04 then docs/05 (mandatory steps only)
```

To wipe a previous lab install before retrying, use the cleanup section at the end of [05](./docs/05-deploy-and-verify.md).

## Concepts in one line

| Acronym | Meaning |
|---------|---------|
| **JOSDK** | Java Operator SDK — the general Java operator framework |
| **QOSDK** | Quarkus Operator SDK — Quarkus extension that wraps JOSDK (CDI, BOM, scaffolding) |

## Optional next steps

When you finish the Joke 101 path, explore a richer community operator:

- [OpenShift Integration Operator](https://github.com/maximilianoPizarro/openshift-integration-operator) (Apache 2.0 · OperatorHub)

## Links

- [OpenShift Local](https://developers.redhat.com/products/openshift-local)
- [QOSDK documentation](https://docs.quarkiverse.io/quarkus-operator-sdk/dev/)
- [Joke sample (upstream)](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke)
- [Quarkus Club](https://www.youtube.com/live/WwMOUMQyq4s)
- [Author on LinkedIn](https://www.linkedin.com/in/maximiliano-gregorio-pizarro-consultor-it/)
- [Author on GitHub](https://github.com/maximilianoPizarro)

## License

Tutorial and slides in this repository are provided for community learning. Third-party projects retain their own licenses (Apache 2.0 for Quarkus / QOSDK samples unless noted otherwise).
