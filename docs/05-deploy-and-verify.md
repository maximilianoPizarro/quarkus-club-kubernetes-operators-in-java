# 05 — Deploy and verify

**Estimated time: 15–20 minutes**

Goal: install the Joke operator with **`operator-sdk run bundle`**, create a JokeRequest, and confirm reconciliation.

**Prerequisite:** chapter 04 mandatory steps finished — both ImageStreams exist:

```bash
oc get is -n joke-operator-demo
# must show joke-operator:1.0.0 and joke-operator-bundle:latest
```

```bash
cd joke-operator
oc project joke-operator-demo
REG=$(oc registry info)
BUNDLE_IMG="${REG}/joke-operator-demo/joke-operator-bundle:latest"
```

## Mandatory steps (do in order)

### M5.1 — Pull secret for the internal registry

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

### M5.2 — Install with `operator-sdk run bundle` (Linux / macOS)

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

Success looks like:

```text
OLM has successfully installed "joke-operator.v1.0.0-snapshot"
```

#### Windows alternative — run operator-sdk inside the CRC VM

Windows Podman Machine often needs Hyper-V admin rights. OpenShift Local exposes Podman over SSH on port `2222`.

One-time setup (Git Bash / PowerShell):

```bash
CRC_SSH_KEY="$HOME/.crc/machines/crc/id_ed25519"
# curl -fL -o operator-sdk-linux \
#   https://github.com/operator-framework/operator-sdk/releases/download/v1.42.3/operator-sdk_linux_amd64

scp -P 2222 -i "$CRC_SSH_KEY" operator-sdk-linux core@127.0.0.1:~/operator-sdk
oc config view --raw --minify > /tmp/crc-kubeconfig.yaml
scp -P 2222 -i "$CRC_SSH_KEY" /tmp/crc-kubeconfig.yaml core@127.0.0.1:~/kubeconfig
scp -P 2222 -i "$CRC_SSH_KEY" /tmp/crc-pull-secret.json core@127.0.0.1:~/pull-secret.json

ssh -i "$CRC_SSH_KEY" -p 2222 -o StrictHostKeyChecking=no core@127.0.0.1
```

Inside the CRC VM:

```bash
chmod +x ~/operator-sdk
export KUBECONFIG=$HOME/kubeconfig
TOKEN=<paste from host: oc whoami -t>
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

### M5.3 — Verify OLM install

```bash
oc get csv -n joke-operator-demo
oc get pods -n joke-operator-demo -l app.kubernetes.io/name=joke-operator
oc get catalogsource,subscription,operatorgroup -n joke-operator-demo
oc get crd | grep -i joke
```

Expect CSV phase **Succeeded** and a Running `joke-operator-…` pod.

### M5.4 — Create a JokeRequest and confirm reconcile

```bash
oc apply -n joke-operator-demo -f src/main/k8s/jokerequest.yml

oc get jokerequests -n joke-operator-demo
oc describe jokerequest -n joke-operator-demo
oc get jokes -n joke-operator-demo
# replace <joke-id> with a name from the previous command:
oc get jokes <joke-id> -n joke-operator-demo -o jsonpath="{.joke}{'\n'}"
```

Success criteria:

- `JokeRequest` status shows `State: CREATED` (or `ALREADY_PRESENT`)
- a **Joke** resource holds text from the public Joke API

## Mandatory cleanup (before re-running the lab)

Prefer `operator-sdk cleanup` over deleting individual resources by hand:

```bash
# From the machine where you ran `run bundle` (host or CRC VM)
operator-sdk cleanup joke-operator --namespace joke-operator-demo

oc delete project joke-operator-demo
oc delete crd jokes.samples.javaoperatorsdk.io jokerequests.samples.javaoperatorsdk.io --ignore-not-found

# Wait until the project is fully gone before M4.1 again
oc get project joke-operator-demo 2>&1 || echo "ready to redeploy"
```

Then redo **[04](./04-build-bundle-operator-sdk.md)** (M4.1→M4.5) and this chapter (M5.1→M5.4).

If you only need to reinstall OLM (images already in the registry), recreate the project, re-link the pull secret (M5.1), and run M5.2 again. Rebuild the bundle (M4.5) if you changed the CSV or operator image.

## Optional — Deployment without OLM

If you cannot run `operator-sdk`, you can still exercise reconcile with a plain Deployment pointing at:

`image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator:1.0.0`

Prefer `run bundle` for the OperatorHub / OLM experience.

## You completed the 101 path

You used the committed Joke operator, pushed images to the **internal registry**, installed with **operator-sdk run bundle**, and exercised a reconcile loop.

### Timing overview

| Module | Time |
|--------|------|
| [01 — Prerequisites](./01-prerequisites.md) | 15–20 min |
| [02 — Podman Desktop & OpenShift Local](./02-podman-desktop-openshift-local.md) | 20–30 min |
| [02a — Trust certificates](./02a-trust-openshift-local-certificates.md) | 5–10 min |
| [03 — Joke operator project](./03-scaffold-joke-operator.md) | 5–10 min |
| [04 — Build (internal registry)](./04-build-bundle-operator-sdk.md) | 20–30 min |
| [05 — Deploy and verify](./05-deploy-and-verify.md) | 15–20 min |
| **Total (hands-on)** | **~90–120 min** |

### Optional next step

- [OpenShift Integration Operator](https://github.com/maximilianoPizarro/openshift-integration-operator)

### Slides

- Live: https://maximilianopizarro.github.io/quarkus-club-kubernetes-operators-in-java/
- PDF: [../slides/quarkus-club-operators.pdf](../slides/quarkus-club-operators.pdf)
