This directory is intended for use by developers.

If you want to build an RPM from the current contents of the directory you just
run:

`rpm/build-rpm.sh`

If you want to build an RPM from the content of a given branch or tag or commit
you just run:

`rpm/build-rpm.sh -b $GIT_TREE`

By default the RPM will be built with Centos 8 Stream with EPEL enabled, if you
want to change the mock config you just use:

`rpm/build-rpm.sh -r $MOCK_CONFIG`
