# 05 — Deploy and verify

**Estimated time: 15–20 minutes**

Goal: install the Joke operator on OpenShift Local with **`operator-sdk run bundle`**, create a JokeRequest, and confirm reconciliation.

Stay in the `joke-operator` project directory from chapters 03–04. Images must already be in the OpenShift Local registry (chapter 04).

```bash
oc project joke-operator-demo
REG=$(oc registry info)   # default-route-openshift-image-registry.apps-crc.testing
BUNDLE_IMG="${REG}/joke-operator-demo/joke-operator-bundle:latest"
```

## 1. Pull secret for the internal registry

OLM and `operator-sdk` need credentials to pull from the CRC registry:

```bash
TOKEN=$(oc whoami -t)
AUTH=$(printf 'kubeadmin:%s' "$TOKEN" | base64 | tr -d '\n')
mkdir -p /tmp
cat > /tmp/crc-pull-secret.json <<EOF
{
  "auths": {
    "${REG}": { "auth": "${AUTH}" },
    "image-registry.openshift-image-registry.svc:5000": { "auth": "${AUTH}" }
  }
}
EOF

oc create secret generic crc-pull-secret \
  --from-file=.dockerconfigjson=/tmp/crc-pull-secret.json \
  --type=kubernetes.io/dockerconfigjson \
  -n joke-operator-demo \
  --dry-run=client -o yaml | oc apply -f -

oc secrets link default crc-pull-secret --for=pull -n joke-operator-demo
```

## 2. Install with `operator-sdk run bundle`

### Linux / macOS (local Podman or Docker)

```bash
echo "$TOKEN" | podman login -u kubeadmin --password-stdin --tls-verify=false "$REG"

operator-sdk run bundle "$BUNDLE_IMG" \
  --namespace joke-operator-demo \
  --timeout 10m \
  --security-context-config=restricted \
  --skip-tls-verify \
  --pull-secret-name=crc-pull-secret
```

> Do **not** pass `--use-http` or `--skip-tls` against the CRC registry route — those force plain HTTP and fail with `400 Bad Request`. Use `--skip-tls-verify` only.

### Windows (recommended: run operator-sdk inside the CRC VM)

Windows Podman Machine often needs Hyper-V admin rights. OpenShift Local already exposes Podman over SSH on port `2222`. Copy a Linux `operator-sdk` (and kubeconfig) into the CRC VM once, then run the bundle from there.

```bash
# One-time setup (from Git Bash / PowerShell)
CRC_SSH_KEY="$HOME/.crc/machines/crc/id_ed25519"
# Download Linux binary if needed:
# curl -fL -o operator-sdk-linux \
#   https://github.com/operator-framework/operator-sdk/releases/download/v1.42.3/operator-sdk_linux_amd64

scp -P 2222 -i "$CRC_SSH_KEY" operator-sdk-linux core@127.0.0.1:~/operator-sdk
oc config view --raw --minify > /tmp/crc-kubeconfig.yaml
scp -P 2222 -i "$CRC_SSH_KEY" /tmp/crc-kubeconfig.yaml core@127.0.0.1:~/kubeconfig
scp -P 2222 -i "$CRC_SSH_KEY" /tmp/crc-pull-secret.json core@127.0.0.1:~/pull-secret.json
```

```bash
ssh -i "$CRC_SSH_KEY" -p 2222 -o StrictHostKeyChecking=no core@127.0.0.1
```

Inside the CRC VM:

```bash
chmod +x ~/operator-sdk
export KUBECONFIG=$HOME/kubeconfig
TOKEN=$(~/kubectl create token -n joke-operator-demo --duration=1h 2>/dev/null || true)
# Or paste the same TOKEN from `oc whoami -t` on the host:
# TOKEN=<from host>

REG=default-route-openshift-image-registry.apps-crc.testing
BUNDLE_IMG=${REG}/joke-operator-demo/joke-operator-bundle:latest

echo "$TOKEN" | podman login -u kubeadmin --password-stdin --tls-verify=false "$REG"

~/operator-sdk run bundle "$BUNDLE_IMG" \
  --namespace joke-operator-demo \
  --timeout 10m \
  --security-context-config=restricted \
  --skip-tls-verify \
  --pull-secret-name=crc-pull-secret
```

Success looks like:

```text
OLM has successfully installed "joke-operator.v1.0.0-snapshot"
```

## 3. Verify OLM install

```bash
oc get csv -n joke-operator-demo
oc get pods -n joke-operator-demo
oc get catalogsource,subscription,operatorgroup -n joke-operator-demo
oc get crd | grep -i joke
```

Expect CSV phase **Succeeded** and a Running `joke-operator-…` pod.

## 4. Create a JokeRequest

```bash
oc apply -n joke-operator-demo -f src/main/k8s/jokerequest.yml

oc get jokerequests -n joke-operator-demo
oc describe jokerequest -n joke-operator-demo
oc get jokes -n joke-operator-demo
oc get jokes <joke-id> -n joke-operator-demo -o jsonpath="{.joke}{'\n'}"
```

When reconcile succeeds:

- `JokeRequest` status shows `State: CREATED`
- a **Joke** resource holds the text from the public Joke API

## 5. Cleanup (before re-running the lab)

From the machine where you ran `run bundle` (host or CRC VM):

```bash
operator-sdk cleanup joke-operator --namespace joke-operator-demo
# CRC VM example:
# ~/operator-sdk cleanup joke-operator --namespace joke-operator-demo
```

Then remove namespace leftovers and CRDs:

```bash
oc delete project joke-operator-demo
oc delete crd jokes.samples.javaoperatorsdk.io jokerequests.samples.javaoperatorsdk.io --ignore-not-found
```

Optionally delete your local scaffold (gitignored):

```bash
rm -rf ~/joke-operator /tmp/quarkus-operator-sdk
```

## Fallback — Deployment without OLM

If you cannot run `operator-sdk` (no Podman / CRC SSH), you can still exercise reconcile with a plain Deployment. See the previous lab notes or apply CRDs + RBAC + Deployment pointing at:

`image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator:1.0.0`

Prefer `run bundle` for the OperatorHub / OLM experience.

## You completed the 101 path

You installed OpenShift Local, pushed images to the **internal registry**, installed the operator with **operator-sdk run bundle**, and exercised a reconcile loop with a simple CR.

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
