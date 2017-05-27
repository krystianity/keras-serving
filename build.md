# tensorflow serving build troubleshoot
* per default running ./prepare.sh will build the model-server image locally
* it takes about 15 minutes to prepare and about 20 minutes to compile tensorflow and the server
on a workstation (about 2,5 hours on a vm)
* per default the image will try to allocate 4GB Memory and all CPU there is to bazel during 
the compilation
* bazel sometimes fails during dependency downloads if a mirror is unreachable, you might just try to re-run
`./prepare.sh` after a few minutes
