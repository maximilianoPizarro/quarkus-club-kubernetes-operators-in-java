# 03 — Scaffold the Joke operator

Goal: get a minimal QOSDK operator on disk — the Quarkiverse **Joke** sample (hello-world for Java operators).

## JOSDK vs QOSDK (30 seconds)

- **JOSDK** (Java Operator SDK) is the general Java framework for reconcile loops, informers, and CRD-backed controllers.
- **QOSDK** (Quarkus Operator SDK) is the Quarkus extension that wraps JOSDK so reconcilers are CDI beans, versions align with the Quarkus BOM, and you can scaffold from `code.quarkus.io` / the Quarkus CLI.

This 101 path uses **QOSDK** so the operator feels like any other Quarkus app.

## Option A — Clone the Joke sample (fastest)

```bash
git clone https://github.com/quarkiverse/quarkus-operator-sdk.git
cd quarkus-operator-sdk/samples/joke
```

Upstream sample: [quarkus-operator-sdk/samples/joke](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke).

## Option B — Scaffold with Quarkus CLI

```bash
quarkus create app org.acme:joke-operator \
  --extension='quarkus-operator-sdk,quarkus-operator-sdk-bundle-generator'
cd joke-operator
```

Then either adapt the generated stubs to match the Joke CR pattern, or prefer Option A so the CRD and reconciler are already complete.

You can also start from [code.quarkus.io](https://code.quarkus.io) and search for **qosdk** / **operator**.

## What you should see

- A Maven Quarkus project with QOSDK dependencies.
- Custom resources: you create a **JokeRequest**; the reconciler may create a **Joke** with the fetched text.
- Sample apply file: `src/main/k8s/jokerequest.yml`.
- With the **bundle-generator** extension: OLM manifests produced on `mvn package`.

## Local smoke test (optional, without OLM)

With `oc` pointed at OpenShift Local:

```bash
# from quarkus-operator-sdk repo root if building the multi-module project:
# mvn -Dquickly -Dquarkus.operator-sdk.crd.apply=true
cd samples/joke
./mvnw package
./mvnw quarkus:dev
# in another terminal:
oc apply -f src/main/k8s/jokerequest.yml
oc get jokerequests
oc get jokes
```

The OLM path in the next chapters is what you use for a “real” install via `operator-sdk run bundle`.

## Next

→ [04 — Build the OLM bundle with operator-sdk](./04-build-bundle-operator-sdk.md)
