# tensorflow serving build troubleshoot
* per default running ./prepare.sh will build the model-server image locally
* it takes about 15 minutes to prepare and about 20 minutes to compile tensorflow and the server
on a workstation (about 2,5 hours on a vm)
* per default the image will try to allocate 4GB Memory and all CPU there is to bazel during 
the compilation
* if you dont want to wait, dont have the computing power OR have re-occuring compilation errors
you can replace `FROM tf-model-server` with `FROM krystianity/keras-serving` in `/Dockerfile` and
simple ignore the build of the image locally (be aware that you will have to download ~ 3.5GB docker layers
this way)
* bazel sometimes fails during dependency downloads if a mirror is unreachable, you might just try to re-run
`./prepare.sh` after a few minutes