#!/bin/bash
set -eo pipefail

# enables building the test-deployment container with the same script
# defaults to packages for minimal intervention in the ci config
FOLDER="${FOLDER:-server}"

DOCKER_IMAGE_TAG="speckle/img2pc"

if [[ "${CIRCLE_TAG}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    IMAGE_VERSION_TAG="${CIRCLE_TAG}"
else
    #shellcheck disable=SC2046
    LAST_RELEASE="$(git describe --always --tags $(git rev-list --tags) | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | head -n 1 || echo "0.0.0")"
    NEXT_RELEASE="$(echo "${LAST_RELEASE}" | python -c "parts = input().split('.'); parts[-1] = str(int(parts[-1])+1); print('.'.join(parts))")"
    BRANCH_NAME_TRUNCATED="$(echo "${CIRCLE_BRANCH}" | cut -c -50 | sed 's/[^a-zA-Z0-9_.-]/_/g')" # docker has a 128 character tag limit, so ensuring the branch name will be short enough
    IMAGE_VERSION_TAG="$NEXT_RELEASE-branch.${BRANCH_NAME_TRUNCATED}"
fi

echo "🧱 Building image: ${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}"

export DOCKER_BUILDKIT=1

docker build --tag "${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}" --file "${FOLDER}/Dockerfile" .

echo "Starting tagging & publishing of image: ${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}"

echo "🐳 Logging into Docker"
echo "${DOCKER_REG_PASS}" | docker login -u "${DOCKER_REG_USER}" --password-stdin "${DOCKER_REG_URL}"

echo "⏫ Pushing loaded image: '${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}'"
docker push "${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}"

if [[ "${IMAGE_VERSION_TAG}" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "🏷 Tagging and pushing image as '${DOCKER_IMAGE_TAG}:latest'"
  docker tag "${DOCKER_IMAGE_TAG}:${IMAGE_VERSION_TAG}" "${DOCKER_IMAGE_TAG}:latest"
  docker push "${DOCKER_IMAGE_TAG}:latest"
fi

echo "✅ Publishing completed."
