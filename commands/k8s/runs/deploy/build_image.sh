# k8s에서 사용 할 automate eventstorming generator 이미지를 빌드 후 푸시
# bash .\commands\k8s\runs\deploy\build_image.sh

docker build -t asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest . --no-cache
docker push asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest