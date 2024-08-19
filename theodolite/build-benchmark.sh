kubectl delete cm resnet-system-configmap
kubectl delete -f benchmark.yml
kubectl create cm resnet-system-configmap --from-file ../manifests
kubectl apply -f benchmark.yml
sleep 3
kubectl get benchmarks