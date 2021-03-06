# Development

In addition to the MLT prerequisites, developer builds require the
following:
* [tox](http://tox.readthedocs.io/en/latest/install.html)

To get set up, please run the following command:

`make dev-env`

This command will create an editable install of your `mlt` repository.
To install specifically with `Python3` version, set `PY` variable and run the command as follows:

`PY=3 make dev-env`

You can then set up an alias to `mlt` as below, so you don't have to activate your .venv/.venv3 if you don't want to.

`alias mlt='/Users/robertso/mlt/.venv/bin/mlt'`

You can put this alias in your `~/.bash_profile` or similar file.

Then you can run `mlt` from anywhere and it'll run your current repository codebase.

#### NOTE: If you run any test locally, you'll need to redo the dev-env because tests install non-editable versions of mlt

# Testing

### E2E Testing Options

`make test-e2e`: Use docker-compose to spin up a testing container and run tests.
This is used by circleci to run tests on a Google Cloud test cluster.

`make test-e2e-no-docker`: Use your local environment to run e2e tests, similar to the way `make test` runs unit tests.
Developers should use this option.

### External Container Registry

```
EXTRA_ARGS=`$MLT_REGISTRY_AUTH_COMMAND` make test-e2e-no-docker
```

where `$MLT_REGISTRY_AUTH_COMMAND` is something like presented below, which you can put in a `~/.bash_profile` or similar file.

`export MLT_REGISTRY_AUTH_COMMAND="gcloud container clusters get-credentials {location} --zone {zone} --project {projectname}"`

You will also need the environment variable `MLT_REGISTRY` to be set, something like the following.

`export MLT_REGISTRY=gcr.io/{projectname}`


### Partial Test Running

This will only run the `test_simple_deploy` e2e test.
```
TESTFILES=tests/e2e/test_deploy_flow.py::test_simple_deploy make test...
```


### Passing extra opts to a test (unit or e2e)

```
TESTOPTS='-s' make test
```
