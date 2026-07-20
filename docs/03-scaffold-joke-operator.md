# 03 — Scaffold the Joke operator

**Estimated time: 10–15 minutes**

Goal: get a minimal QOSDK operator on disk — the Quarkiverse **Joke** sample (hello-world for Java operators).

Do this work **outside** this tutorial repository (or in a gitignored folder). The repo `.gitignore` already excludes `joke-operator/` and `quarkus-operator-sdk/` so cloned/scaffolded code is not committed by mistake.

## JOSDK vs QOSDK (30 seconds)

- **JOSDK** (Java Operator SDK) is the general Java framework for reconcile loops, informers, and CRD-backed controllers.
- **QOSDK** (Quarkus Operator SDK) is the Quarkus extension that wraps JOSDK so reconcilers are CDI beans, versions align with the Quarkus BOM, and you can scaffold from `code.quarkus.io` / the Quarkus CLI.

This 101 path uses **QOSDK** so the operator feels like any other Quarkus app.

## Recommended — Scaffold with Quarkus CLI + Joke sample sources

Create a standalone Quarkus app (released BOM versions), then copy the Joke sample sources so you do not need to build the whole QOSDK multi-module SNAPSHOT tree.

```bash
# From your home directory (or any folder outside this docs repo)
quarkus create app org.acme:joke-operator \
  --extension='quarkus-operator-sdk,quarkus-operator-sdk-bundle-generator,rest-jackson,rest-client-jackson,container-image-jib,kubernetes' \
  --no-code
cd joke-operator
```

Clone the upstream sample **only to copy sources** (do not commit that clone into the tutorial repo):

```bash
git clone --depth 1 https://github.com/quarkiverse/quarkus-operator-sdk.git /tmp/quarkus-operator-sdk
SAMPLE=/tmp/quarkus-operator-sdk/samples/joke

mkdir -p src/main/java/io/quarkiverse/operatorsdk/samples/joke
cp "$SAMPLE"/src/main/java/io/quarkiverse/operatorsdk/samples/joke/*.java \
  src/main/java/io/quarkiverse/operatorsdk/samples/joke/

mkdir -p src/main/k8s src/main/kubernetes
cp "$SAMPLE"/src/main/k8s/jokerequest.yml src/main/k8s/
cp "$SAMPLE"/src/main/kubernetes/icon.png src/main/kubernetes/
```

On Windows Git Bash, use a Windows-friendly clone path if you prefer, for example `C:/Users/$USER/src/quarkus-operator-sdk`.

Configure `src/main/resources/application.properties`:

```properties
joke-api/mp-rest/url=https://v2.jokeapi.dev/joke
quarkus.operator-sdk.crd.apply=true
quarkus.container-image.builder=jib
quarkus.operator-sdk.bundle.channels=alpha
quarkus.operator-sdk.crd.generate-all=true
quarkus.kubernetes-client.devservices.override-kubeconfig=true
quarkus.http.test-port=0
```

Upstream sample reference: [quarkus-operator-sdk/samples/joke](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke).

You can also start from [code.quarkus.io](https://code.quarkus.io) and search for **qosdk** / **operator**.

## Alternative — Build from the cloned multi-module sample

```bash
git clone https://github.com/quarkiverse/quarkus-operator-sdk.git
cd quarkus-operator-sdk
./mvnw -Dquickly
cd samples/joke
```

This builds the SNAPSHOT parent modules first and takes longer. Prefer the Quarkus CLI path above for workshops.

## What you should see

- A Maven Quarkus project with QOSDK dependencies.
- Custom resources: you create a **JokeRequest**; the reconciler may create a **Joke** with the fetched text.
- Sample apply file: `src/main/k8s/jokerequest.yml`.
- With the **bundle-generator** extension: OLM manifests produced on `mvn package`.

## Local smoke test (optional, without OLM)

With `oc` pointed at OpenShift Local:

```bash
./mvnw package
./mvnw quarkus:dev
# in another terminal:
oc apply -f src/main/k8s/jokerequest.yml
oc get jokerequests
oc get jokes
```

The OLM / registry path in the next chapters is what you use for a cluster install with container images.

## Next

→ [04 — Build images against the OpenShift Local registry](./04-build-bundle-operator-sdk.md)
