def undeploy(args):
    if not os.path.isfile('.studio.json'):
        print("run `mlt undeploy` within a project directory")
        sys.exit(1)

    config = json.load(open('.studio.json'))
    namespace = config['namespace']
    run(["kubectl", "--namespace", namespace, "delete", "-f", "k8s"])