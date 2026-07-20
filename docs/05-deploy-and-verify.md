# 05 — Deploy and verify

**Estimated time: 15–20 minutes**

Goal: install the Joke operator on OpenShift Local from the images in the **internal registry**, create a JokeRequest, and confirm reconciliation.

Stay in the `joke-operator` project directory from chapters 03–04. Namespace: `joke-operator-demo`.

```bash
oc project joke-operator-demo
```

## 1. Apply CRDs

```bash
oc apply -f target/bundle/joke-operator/manifests/jokes.samples.javaoperatorsdk.io-v1.crd.yml
oc apply -f target/bundle/joke-operator/manifests/jokerequests.samples.javaoperatorsdk.io-v1.crd.yml

oc get crd | grep -i joke
```

## 2. RBAC + ServiceAccount

```bash
oc create sa joke-operator -n joke-operator-demo 2>/dev/null || true

cat <<'EOF' | oc apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: joke-operator-permissions
  namespace: joke-operator-demo
rules:
- apiGroups: ["samples.javaoperatorsdk.io"]
  resources: ["jokerequests", "jokerequests/status", "jokerequests/finalizers"]
  verbs: ["get", "list", "watch", "patch", "update", "create", "delete"]
- apiGroups: ["samples.javaoperatorsdk.io"]
  resources: ["jokes"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: joke-operator-permissions
  namespace: joke-operator-demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: joke-operator-permissions
subjects:
- kind: ServiceAccount
  name: joke-operator
  namespace: joke-operator-demo
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: joke-operator-crd-reader
rules:
- apiGroups: ["apiextensions.k8s.io"]
  resources: ["customresourcedefinitions"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: joke-operator-crd-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: joke-operator-crd-reader
subjects:
- kind: ServiceAccount
  name: joke-operator
  namespace: joke-operator-demo
EOF
```

## 3. Deploy the operator

```bash
cat <<'EOF' | oc apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: joke-operator
  namespace: joke-operator-demo
  labels:
    app.kubernetes.io/name: joke-operator
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: joke-operator
  template:
    metadata:
      labels:
        app.kubernetes.io/name: joke-operator
    spec:
      serviceAccountName: joke-operator
      containers:
      - name: joke-operator
        image: image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator:1.0.0
        imagePullPolicy: Always
        env:
        - name: KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        ports:
        - containerPort: 8080
          name: http
        livenessProbe:
          httpGet:
            path: /q/health/live
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /q/health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
EOF

oc rollout status deployment/joke-operator -n joke-operator-demo --timeout=180s
oc get pods -n joke-operator-demo -l app.kubernetes.io/name=joke-operator
oc logs -n joke-operator-demo deploy/joke-operator --tail=40
```

You should see the reconciler registered for namespace `joke-operator-demo`.

### Optional — `operator-sdk run bundle`

If you have a working local container runtime that can pull from the CRC registry route, you can install via OLM instead:

```bash
operator-sdk run bundle \
  default-route-openshift-image-registry.apps-crc.testing/joke-operator-demo/joke-operator-bundle:latest \
  --namespace joke-operator-demo \
  --timeout 10m \
  --skip-tls \
  --use-http
```

Then check:

```bash
oc get csv -n joke-operator-demo
oc get pods -n joke-operator-demo
```

The Deployment path above is the default for this tutorial because it works reliably with only `oc` + the OpenShift Local registry (including on Windows when Podman/Hyper-V needs admin).

## 4. Create a JokeRequest

```bash
oc apply -n joke-operator-demo -f src/main/k8s/jokerequest.yml
```

Watch the request and resulting jokes:

```bash
oc get jokerequests -n joke-operator-demo
oc describe jokerequest -n joke-operator-demo
oc get jokes -n joke-operator-demo

# Once a Joke exists (name is often the joke id from the API):
oc get jokes <joke-id> -n joke-operator-demo -o jsonpath="{.joke}{'\n'}"
```

When reconcile succeeds:

- `JokeRequest` status shows `State: CREATED`
- a **Joke** resource holds the text fetched from the public Joke API

## 5. Cleanup (before re-running the lab)

Remove the demo so the next person (or you) can follow the instructivo from a clean cluster:

```bash
# CRs
oc delete jokerequest --all -n joke-operator-demo --ignore-not-found
oc delete joke --all -n joke-operator-demo --ignore-not-found

# Workloads / OLM leftovers
oc delete deployment joke-operator -n joke-operator-demo --ignore-not-found
oc delete csv -n joke-operator-demo --all --ignore-not-found
# If you used operator-sdk run bundle:
# operator-sdk cleanup joke-operator --namespace joke-operator-demo

# Project (also deletes ImageStreams / Builds in that namespace)
oc delete project joke-operator-demo

# Cluster-scoped leftovers
oc delete crd jokes.samples.javaoperatorsdk.io jokerequests.samples.javaoperatorsdk.io --ignore-not-found
oc delete clusterrole joke-operator-crd-reader --ignore-not-found
oc delete clusterrolebinding joke-operator-crd-reader --ignore-not-found
```

Optionally delete your local scaffold (it is gitignored):

```bash
rm -rf ~/joke-operator /tmp/quarkus-operator-sdk
# Windows Git Bash example:
# rm -rf /c/Users/$USER/joke-operator
```

## You completed the 101 path

You installed OpenShift Local, pushed images to the **internal registry**, deployed a QOSDK operator, and exercised a reconcile loop with a simple CR.

### Timing overview

| Module | Time |
|--------|------|
| [01 — Prerequisites](./01-prerequisites.md) | 15–20 min |
| [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md) | 20–30 min |
| [02a — Trust certificates](./02a-trust-openshift-local-certificates.md) | 5–10 min |
| [03 — Scaffold](./03-scaffold-joke-operator.md) | 10–15 min |
| [04 — Build (internal registry)](./04-build-bundle-operator-sdk.md) | 20–30 min |
| [05 — Deploy and verify](./05-deploy-and-verify.md) | 15–20 min |
| **Total (hands-on)** | **~90–120 min** |

### Optional next step

Explore a richer community operator on OperatorHub:

- [OpenShift Integration Operator](https://github.com/maximilianoPizarro/openshift-integration-operator)

### Slides

- Live: https://maximilianopizarro.github.io/quarkus-club-kubernetes-operators-in-java/
- PDF: [../slides/quarkus-club-operators.pdf](../slides/quarkus-club-operators.pdf)
