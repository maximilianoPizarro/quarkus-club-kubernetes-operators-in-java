# joke-operator

QOSDK sample operator used by the [Quarkus Club — Kubernetes Operators in Java](../README.md) tutorial.

Creates a `Joke` custom resource when you apply a `JokeRequest` (text from [JokeAPI](https://v2.jokeapi.dev/)).

## Workshop path (recommended)

Follow the docs from the repository root — do **not** re-scaffold unless you want the optional from-scratch exercise:

1. [03 — Joke operator project](../docs/03-scaffold-joke-operator.md)
2. [04 — Build against OpenShift Local registry](../docs/04-build-bundle-operator-sdk.md) (**mandatory:** operator image + bundle image)
3. [05 — Deploy and verify](../docs/05-deploy-and-verify.md)

```bash
cd joke-operator
# then M4.* / M5.* from the docs
```

## Workshop fixes in this tree

- Kubernetes Dev Services disabled (uses OpenShift Local kubeconfig).
- `JokeReconciler` so the `Joke` CRD is **owned** in the OLM CSV.
- Install modes: `OwnNamespace`, `SingleNamespace`, `AllNamespaces`.

Upstream reference: [quarkiverse/quarkus-operator-sdk samples/joke](https://github.com/quarkiverse/quarkus-operator-sdk/tree/main/samples/joke).

## Dev mode (optional)

```bash
./mvnw quarkus:dev
```

Requires a working `oc`/kubeconfig against OpenShift Local (or another cluster).
