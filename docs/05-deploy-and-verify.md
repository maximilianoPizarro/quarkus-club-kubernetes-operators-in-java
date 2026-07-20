# 05 — Deploy and verify

Goal: install the Joke operator on OpenShift Local with **operator-sdk**, create a Joke CR, and confirm reconciliation.

## Namespace

```bash
oc new-project joke-operator-demo
# or
oc create namespace joke-operator-demo
oc project joke-operator-demo
```

## Install from the bundle

Point `operator-sdk` at your bundle image (local or remote):

```bash
operator-sdk run bundle \
  quay.io/YOUR_USER/joke-operator-bundle:v0.0.1 \
  --namespace joke-operator-demo \
  --timeout 10m
```

Wait until the ClusterServiceVersion (CSV) succeeds and the operator pod is Running:

```bash
oc get csv -n joke-operator-demo
oc get pods -n joke-operator-demo
oc get crd | grep -i joke
```

## Create a JokeRequest

The Joke sample watches **JokeRequest** CRs. Apply the sample manifest from the project:

```bash
oc apply -n joke-operator-demo -f src/main/k8s/jokerequest.yml
```

Watch the request and resulting jokes:

```bash
oc get jokerequests -n joke-operator-demo -w
oc describe jokerequest -n joke-operator-demo
oc get jokes -n joke-operator-demo
# Once a Joke exists (name is often the joke id from the API):
oc get jokes <joke-id> -n joke-operator-demo -o jsonpath="{.joke}{'\n'}"
```

When reconcile succeeds, a **Joke** resource holds the joke text fetched from the public Joke API.

## Cleanup

```bash
operator-sdk cleanup <operator-package-name> --namespace joke-operator-demo
oc delete project joke-operator-demo
```

Or delete the CSV / subscription resources created by `run bundle`, then remove leftover CRDs if you no longer need them.

## You completed the 101 path

You installed OpenShift Local, built a QOSDK operator bundle, deployed it with operator-sdk, and exercised a reconcile loop with a simple CR.

### Optional next step

Explore a richer community operator on OperatorHub:

- [OpenShift Integration Operator](https://github.com/maximilianoPizarro/openshift-integration-operator)

### Slides

- Live: https://maximilianopizarro.github.io/quarkus-club-kubernetes-operators-in-java/
- PDF: [../slides/quarkus-club-operators.pdf](../slides/quarkus-club-operators.pdf)
