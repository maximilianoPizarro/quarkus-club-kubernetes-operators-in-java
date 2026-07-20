# 04 — Build the OLM bundle with operator-sdk

Goal: produce a valid OLM **bundle** image for the Joke operator and validate it with **operator-sdk**.

QOSDK docs: [Deploy with OLM](https://docs.quarkiverse.io/quarkus-operator-sdk/dev/deploy-with-olm.html).

## Ensure the bundle-generator extension is present

In `pom.xml` (or when scaffolding), include:

```text
quarkus-operator-sdk-bundle-generator
```

Joke sample builds already include QOSDK; confirm the bundle generator is enabled for your chosen module.

## Build the operator and bundle metadata

From the Joke sample (or your scaffolded project) directory:

```bash
./mvnw clean package \
  -Dquarkus.container-image.build=true \
  -Dquarkus.operator-sdk.bundle.channels=alpha
```

Adjust container image coordinates for your registry if you push remotely, for example:

```bash
./mvnw clean package \
  -Dquarkus.container-image.build=true \
  -Dquarkus.container-image.registry=quay.io \
  -Dquarkus.container-image.group=YOUR_USER \
  -Dquarkus.operator-sdk.bundle.channels=alpha
```

Typical outputs:

- Operator container image (Jib / Docker / Podman, depending on config)
- `target/bundle/<operator-name>/manifests/`
- `target/bundle/<operator-name>/bundle.Dockerfile` (or equivalent)

## Validate with operator-sdk

```bash
operator-sdk bundle validate target/bundle/<operator-name> \
  --select-optional name=operatorhub
```

Fix any reported errors before continuing.

## Build the bundle image

```bash
podman build -f target/bundle/<operator-name>/bundle.Dockerfile \
  -t quay.io/YOUR_USER/joke-operator-bundle:v0.0.1 \
  target/bundle/<operator-name>
```

For a fully local OpenShift Local workflow you can tag for a local registry or use the image name that `operator-sdk run bundle` expects on your machine. Push only if your cluster pulls from a remote registry:

```bash
podman push quay.io/YOUR_USER/joke-operator-bundle:v0.0.1
```

## Next

→ [05 — Deploy and verify](./05-deploy-and-verify.md)
