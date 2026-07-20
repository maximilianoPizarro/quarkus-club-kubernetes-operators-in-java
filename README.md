# Quarkus Club — Kubernetes Operators in Java

Hands-on tutorial and presentation slides for the Quarkus Club session on building Kubernetes operators with **Quarkus** and the **Java Operator SDK (JOSDK)** / **Quarkus Operator SDK (QOSDK)**.

This repository walks you from installing **Podman Desktop** and **[OpenShift Local](https://developers.redhat.com/products/openshift-local)** through deploying a simple **Joke** operator — a 101 path anyone can reproduce with a free [Red Hat Developer](https://developers.redhat.com/) account.

Images are built and stored in the **OpenShift Local internal registry** (no Quay account required for the lab).

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

## Tutorial (101 path)

Follow these docs in order. The example uses the Quarkiverse **Joke** sample — not a production integration operator.

Scaffolded / cloned project trees (`joke-operator/`, `quarkus-operator-sdk/`) are **gitignored** — create them while following the docs; do not commit them back to this repository.

| # | Module | Time |
|---|--------|------|
| 1 | [Prerequisites](./docs/01-prerequisites.md) | 15–20 min |
| 2 | [Podman Desktop & OpenShift Local](./docs/02-podman-desktop-openshift-local.md) | 20–30 min |
| 2a | [Trust OpenShift Local certificates](./docs/02a-trust-openshift-local-certificates.md) | 5–10 min |
| 3 | [Scaffold the Joke operator](./docs/03-scaffold-joke-operator.md) | 10–15 min |
| 4 | [Build against the OpenShift Local registry](./docs/04-build-bundle-operator-sdk.md) | 20–30 min |
| 5 | [Deploy and verify](./docs/05-deploy-and-verify.md) | 15–20 min |
| | **Total hands-on** | **~90–120 min** |

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
- [Joke sample](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke)
- [Quarkus Club](https://www.youtube.com/live/WwMOUMQyq4s)
- [Author on LinkedIn](https://www.linkedin.com/in/maximiliano-gregorio-pizarro-consultor-it/)
- [Author on GitHub](https://github.com/maximilianoPizarro)

## License

Tutorial and slides in this repository are provided for community learning. Third-party projects retain their own licenses (Apache 2.0 for Quarkus / QOSDK samples unless noted otherwise).
