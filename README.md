# Quarkus Club — Kubernetes Operators in Java

Hands-on tutorial and presentation slides for the Quarkus Club session on building Kubernetes operators with **Quarkus** and the **Java Operator SDK (JOSDK)** / **Quarkus Operator SDK (QOSDK)**.

This repository walks you from installing **Podman Desktop** and **[OpenShift Local](https://developers.redhat.com/products/openshift-local)** through deploying a simple **Joke** operator with **operator-sdk** — a 101 path anyone can reproduce with a free [Red Hat Developer](https://developers.redhat.com/) account.

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

1. [Prerequisites](./docs/01-prerequisites.md)
2. [Podman Desktop & OpenShift Local](./docs/02-podman-desktop-openshift-local.md)
3. [Scaffold the Joke operator](./docs/03-scaffold-joke-operator.md)
4. [Build the OLM bundle with operator-sdk](./docs/04-build-bundle-operator-sdk.md)
5. [Deploy and verify](./docs/05-deploy-and-verify.md)

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
