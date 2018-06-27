set -e

echo "Experiment:"
kubectl get experiment ${JOB_NAME} --namespace ${NAMESPACE}
printf "\nJobs:\n"
kubectl get jobs -l experiment_name=${JOB_NAME} --namespace ${NAMESPACE}
printf "\nPods:\n"
job_list="$(kubectl get jobs -l experiment_name=${JOB_NAME} --output=jsonpath={.items..metadata.name})"
job_list=${job_list// /, }
pod_command="kubectl get pods -a -l 'job-name in (${job_list})' --namespace ${NAMESPACE}"
eval ${pod_command}
printf "\nResults:\n"
kubectl get results -l experiment=${JOB_NAME} --namespace ${NAMESPACE}
