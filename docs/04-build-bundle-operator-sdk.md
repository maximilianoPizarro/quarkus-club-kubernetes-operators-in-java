# 04 — Build images against the OpenShift Local registry

**Estimated time: 20–30 minutes**

Goal: build the Joke **operator image** and OLM **bundle image** in the **OpenShift Local internal registry** (no Quay account).

QOSDK docs: [Deploy with OLM](https://docs.quarkiverse.io/quarkus-operator-sdk/dev/deploy-with-olm.html).

Work from the committed project:

```bash
cd joke-operator   # repo root → joke-operator/
```

## Mandatory steps (do in order)

You need **both** images before chapter 05:

1. Operator image → `…/joke-operator-demo/joke-operator:1.0.0`
2. Bundle image → `…/joke-operator-demo/joke-operator-bundle:latest`

Skipping **M4.5** is the most common failure (`bundle:latest: not found` on `run bundle`).

### M4.1 — Create the OpenShift project

```bash
oc new-project joke-operator-demo
# if it already exists:
# oc project joke-operator-demo

REG=$(oc registry info)          # e.g. default-route-openshift-image-registry.apps-crc.testing
TOKEN=$(oc whoami -t)
echo "Registry: $REG"
```

### M4.2 — Registry credentials for Jib

```bash
oc policy add-role-to-user registry-editor "$(oc whoami)" -n joke-operator-demo

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

### M4.3 — Build and push the operator image + generate the bundle

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

Expected:

- ImageStream `joke-operator` tag `1.0.0`
- Bundle files under `target/bundle/joke-operator/` (`manifests/`, `bundle.Dockerfile`, `metadata/`)

```bash
oc get is -n joke-operator-demo
```

### M4.4 — Point the CSV at the in-cluster registry URL

Pods pull from the **service** hostname, not the external route:

```bash
CSV=target/bundle/joke-operator/manifests/joke-operator.clusterserviceversion.yaml

# Do not write a .bak inside manifests/ — operator-sdk treats extra YAML as a second CSV.
sed -i \
  's|default-route-openshift-image-registry.apps-crc.testing/|image-registry.openshift-image-registry.svc:5000/|g' \
  "$CSV"

grep 'image:' "$CSV"
```

You must see:

```text
image: image-registry.openshift-image-registry.svc:5000/joke-operator-demo/joke-operator:1.0.0
```

Validate:

```bash
operator-sdk bundle validate target/bundle/joke-operator
```

Warnings about `annotations` / `minKubeVersion` are OK. **Errors** must be fixed before continuing.

### M4.5 — Build the bundle image (in-cluster)

```bash
BUNDLE_DIR=target/bundle/joke-operator
cp "$BUNDLE_DIR/bundle.Dockerfile" "$BUNDLE_DIR/Dockerfile"

oc new-build --name=joke-operator-bundle --binary --strategy=docker \
  -n joke-operator-demo
# If the BuildConfig already exists, skip new-build and only run start-build:

oc start-build joke-operator-bundle \
  --from-dir="$BUNDLE_DIR" \
  --follow \
  -n joke-operator-demo
```

Confirm **both** ImageStreams:

```bash
oc get is -n joke-operator-demo
# joke-operator          …   1.0.0
# joke-operator-bundle   …   latest
```

Bundle image name for chapter 05:

```bash
echo "${REG}/joke-operator-demo/joke-operator-bundle:latest"
```

## Optional — Build the bundle with local Podman

```bash
podman build -f target/bundle/joke-operator/bundle.Dockerfile \
  -t "$REG/joke-operator-demo/joke-operator-bundle:latest" \
  target/bundle/joke-operator

podman push --tls-verify=false \
  "$REG/joke-operator-demo/joke-operator-bundle:latest"
```

## Optional — Quay (not required for this tutorial)

```bash
./mvnw clean package \
  -Dquarkus.container-image.build=true \
  -Dquarkus.container-image.push=true \
  -Dquarkus.container-image.registry=quay.io \
  -Dquarkus.container-image.group=YOUR_USER \
  -Dquarkus.operator-sdk.bundle.channels=alpha
```

## Next

→ [05 — Deploy and verify](./05-deploy-and-verify.md)
