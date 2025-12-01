# 푸시된 이미지를 활용해서 k8s에 배포(재배포)
# bash .\commands\k8s\runs\deploy\apply_to_k8s.sh

kubectl delete deployment.apps/eventstorming-generator
kubectl apply -f k8s/deployment.yaml