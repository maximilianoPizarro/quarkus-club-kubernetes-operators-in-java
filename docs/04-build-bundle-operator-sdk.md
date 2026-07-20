# 04 — Build images against the OpenShift Local registry

**Estimated time: 20–30 minutes**

Goal: build the Joke **operator image** and OLM **bundle** using the **OpenShift Local internal registry** (no Quay account).

QOSDK docs: [Deploy with OLM](https://docs.quarkiverse.io/quarkus-operator-sdk/dev/deploy-with-olm.html).

## Ensure the bundle-generator extension is present

In `pom.xml` (or when scaffolding), include:

```text
quarkus-operator-sdk-bundle-generator
```

Also keep `quarkus-container-image-jib` so Maven can build/push without a local Docker daemon.

## 1. Create the project and log in to the registry

```bash
oc new-project joke-operator-demo
# or: oc project joke-operator-demo

REG=$(oc registry info)          # e.g. default-route-openshift-image-registry.apps-crc.testing
TOKEN=$(oc whoami -t)
echo "Registry: $REG"
```

Grant push rights (kubeadmin usually already can; safe to re-run):

```bash
oc policy add-role-to-user registry-editor "$(oc whoami)" -n joke-operator-demo
```

Configure credentials for Jib (writes `~/.docker/config.json`):

```bash
mkdir -p "$HOME/.docker"
AUTH=$(printf 'kubeadmin:%s' "$TOKEN" | base64 | tr -d '\n')
cat > "$HOME/.docker/config.json" <<EOF
{
  "auths": {
    "${REG}": {
      "auth": "${AUTH}"
    }
  }
}
EOF
```

> On Windows PowerShell, create the same JSON under `%USERPROFILE%\.docker\config.json` with `auth` = Base64 of `kubeadmin:<token>`.

## 2. Build the operator image and generate the bundle

From the `joke-operator` project directory:

```bash
./mvnw clean package \
  -DskipTests \
  -Dquarkus.container-image.build=true \
  -Dquarkus.container-image.push=true \
  -Dquarkus.container-image.insecure=true \
  -Dquarkus.container-image.registry="$REG" \
  -Dquarkus.container-image.group=joke-operator-demo \
  -Dquarkus.container-image.name=joke-operator \
  -Dquarkus.container-image.tag=1.0.0 \
  -Dquarkus.kubernetes.namespace=joke-operator-demo \
  -Dquarkus.operator-sdk.bundle.channels=alpha \
  -Dquarkus.operator-sdk.crd.apply=false
```

Typical outputs:

- Operator image pushed to  
  `default-route-openshift-image-registry.apps-crc.testing/joke-operator-demo/joke-operator:1.0.0`
- Bundle metadata under `target/bundle/joke-operator/`
  - `manifests/`
  - `bundle.Dockerfile`
  - `metadata/`

Verify the ImageStream:

```bash
oc get is -n joke-operator-demo
```

## 3. Point the CSV at the in-cluster registry URL

Pods inside OpenShift pull from the **service** hostname, not the external route. Patch the generated CSV before building the bundle image:

```bash
CSV=target/bundle/joke-operator/manifests/joke-operator.clusterserviceversion.yaml

# Linux / Git Bash / macOS
# Do not write a .bak inside manifests/ — operator-sdk treats extra YAML as a second CSV.
sed -i \
  's|default-route-openshift-image-registry.apps-crc.testing/|image-registry.openshift-image-registry.svc:5000/|g' \
  "$CSV"

grep 'image:' "$CSV"
```

You should see:

```text
image: image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator:1.0.0
```

### Install modes (OwnNamespace)

The reconciler watches the current namespace. If the CSV only enables `AllNamespaces`, OLM will fail with `UnsupportedOperatorGroup` when you use a namespaced OperatorGroup. Ensure `installModes` includes `OwnNamespace` / `SingleNamespace` as supported (edit the CSV if needed).

## 4. Validate with operator-sdk

```bash
operator-sdk bundle validate target/bundle/joke-operator
```

Fix reported errors before continuing. Optional OperatorHub checks:

```bash
operator-sdk bundle validate target/bundle/joke-operator \
  --select-optional name=operatorhub
```

> If validation complains that the `Joke` CRD is in the bundle but not listed as **owned**, move that CRD from `required` to `owned` in the CSV (the sample treats Joke as a secondary CR created by the reconciler).

## 5. Build the bundle image (in-cluster — recommended)

No local Podman/Docker required. Use an OpenShift binary Docker build:

```bash
BUNDLE_DIR=target/bundle/joke-operator
cp "$BUNDLE_DIR/bundle.Dockerfile" "$BUNDLE_DIR/Dockerfile"

oc new-build --name=joke-operator-bundle --binary --strategy=docker \
  -n joke-operator-demo
# If the BuildConfig already exists, skip new-build and only start-build:

oc start-build joke-operator-bundle \
  --from-dir="$BUNDLE_DIR" \
  --follow \
  -n joke-operator-demo
```

Resulting image (in-cluster):

```text
image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator-bundle:latest
```

### Alternative — local Podman

If Podman works on your machine:

```bash
podman build -f target/bundle/joke-operator/bundle.Dockerfile \
  -t "$REG/joke-operator-demo/joke-operator-bundle:1.0.0" \
  target/bundle/joke-operator

podman push --tls-verify=false \
  "$REG/joke-operator-demo/joke-operator-bundle:1.0.0"
```

## Optional — Quay (not required for this tutorial)

If you later publish publicly, swap the registry coordinates for Quay:

```bash
./mvnw clean package \
  -Dquarkus.container-image.build=true \
  -Dquarkus.container-image.push=true \
  -Dquarkus.container-image.registry=quay.io \
  -Dquarkus.container-image.group=YOUR_USER \
  -Dquarkus.operator-sdk.bundle.channels=alpha
```

## Bundle image name for chapter 05

```bash
echo "${REG}/joke-operator-demo/joke-operator-bundle:latest"
# example: default-route-openshift-image-registry.apps-crc.testing/joke-operator-demo/joke-operator-bundle:latest
```

Use that exact string with `operator-sdk run bundle` (HTTPS registry route + `--skip-tls-verify`). Do not use `--use-http`.

## Next

→ [05 — Deploy and verify](./05-deploy-and-verify.md)
