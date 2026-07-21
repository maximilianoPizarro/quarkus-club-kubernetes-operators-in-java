# 03 — Joke operator project

**Estimated time: 5–10 minutes**

Goal: open the **committed** QOSDK Joke operator in this repo and understand what it does before building images.

## Mandatory steps

### M3.1 — Enter the project

```bash
cd joke-operator
```

The sources live under [`joke-operator/`](../joke-operator/) in this repository. **You do not need to clone the Quarkiverse sample** for the 101 path.

### M3.2 — Confirm the layout

You should see:

| Path | Role |
|------|------|
| `src/main/java/.../JokeRequestReconciler.java` | Primary reconciler: creates a `Joke` from the public Joke API |
| `src/main/java/.../JokeReconciler.java` | No-op reconciler so the `Joke` CRD is **owned** in the OLM CSV |
| `src/main/k8s/jokerequest.yml` | Sample CR to apply in chapter 05 |
| `src/main/resources/application.properties` | Dev Services off (uses CRC kubeconfig); CRD generate-all on |
| `pom.xml` | QOSDK + bundle-generator + Jib |

### M3.3 — Know the workshop fixes already applied

Compared with a raw upstream copy, this tree already includes:

1. `quarkus.kubernetes-client.devservices.enabled=false` — use OpenShift Local, not Kind/Testcontainers.
2. `JokeReconciler` — so `operator-sdk bundle validate` accepts the `Joke` CRD as **owned**.
3. CSV `installModes` for `OwnNamespace` / `SingleNamespace` / `AllNamespaces` on `JokeRequestReconciler`.

Skip recreating these by hand unless you follow the optional from-scratch appendix below.

## JOSDK vs QOSDK (30 seconds)

- **JOSDK** (Java Operator SDK) is the general Java framework for reconcile loops, informers, and CRD-backed controllers.
- **QOSDK** (Quarkus Operator SDK) is the Quarkus extension that wraps JOSDK so reconcilers are CDI beans, versions align with the Quarkus BOM, and you can scaffold from `code.quarkus.io` / the Quarkus CLI.

## Optional — Local smoke test (no OLM)

With `oc` already pointed at OpenShift Local:

```bash
./mvnw package
./mvnw quarkus:dev
# in another terminal:
oc apply -f src/main/k8s/jokerequest.yml
oc get jokerequests
oc get jokes
```

The OLM / registry path in chapters 04–05 is the main lab goal.

## Optional appendix — Start from zero (scaffold yourself)

Only if you want to reproduce scaffolding instead of using `joke-operator/` from this repo:

```bash
# Outside this tutorial repo (or any empty folder)
quarkus create app org.acme:joke-operator \
  --extension='quarkus-operator-sdk,quarkus-operator-sdk-bundle-generator,rest-jackson,rest-client-jackson,container-image-jib,kubernetes' \
  --no-code
cd joke-operator

git clone --depth 1 https://github.com/quarkiverse/quarkus-operator-sdk.git /tmp/quarkus-operator-sdk
SAMPLE=/tmp/quarkus-operator-sdk/samples/joke

mkdir -p src/main/java/io/quarkiverse/operatorsdk/samples/joke
cp "$SAMPLE"/src/main/java/io/quarkiverse/operatorsdk/samples/joke/*.java \
  src/main/java/io/quarkiverse/operatorsdk/samples/joke/

mkdir -p src/main/k8s src/main/kubernetes
cp "$SAMPLE"/src/main/k8s/jokerequest.yml src/main/k8s/
cp "$SAMPLE"/src/main/kubernetes/icon.png src/main/kubernetes/
```

Then apply the same workshop fixes listed in **M3.3** (Dev Services off, `JokeReconciler`, install modes). Reference: [quarkus-operator-sdk/samples/joke](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke).

## Next

→ [04 — Build images against the OpenShift Local registry](./04-build-bundle-operator-sdk.md)
