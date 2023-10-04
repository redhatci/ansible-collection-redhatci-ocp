# Storage Service Tests During Upgrade
### Requirements
A default storage class must be defined before running these tests. If the variable `tester_storage_class` is defined, it will use this one instead.
Also, the provisioner associated with this storage class must implement the CSI `CLONE_VOLUME` [capability](https://kubernetes-csi.github.io/docs/developing.html).
For more information on storage classes, see [the OCP documentation](https://docs.openshift.com/container-platform/4.11/post_installation_configuration/storage-configuration.html#defining-storage-classes_post-install-storage-configuration).

### Three scenarios of tests
It can be enabled by setting the boolean `storage_upgrade_tester` to **true**, when the dci-openshift-agent is running an upgrade.
The idea is to test the impact of the cluster upgrade and the storage operator upgrade on the availability on the storage service, which means if volumes can be used normally.
It creates three different k8s CronJob to tests the three different accesses of a PVC:

* *RWO*: ReadWriteOnce, a single pod is trying to bind a volume and write in a file inside it.
* *ROX*: ReadOnlyMany, two pods are bound to the same volume simultaneously and try to read a value inside it.
* *RWX*: ReadWriteMany, two pods are bound to the same volume simultaneously and try to write in a file inside it.

Each cronjob is launching a job every minute, starting just before the upgrade of the platform and results are gathered at the end of the storage service upgrade.
### Test results
The number of files, lines written in the volumes is used to estimate the downtime of the storage service for RWO and RWX cases.
The number of failed ROX jobs is used to estimate this time for ROX use cases.
At the end of the upgrade process, the results are gathered via three bash scripts (one for each test case) `gather-storage-upgrade-tester-ROX.log`, `gather-storage-upgrade-tester-RWO.log`and `gather-storage-upgrade-tester-RWX.log`. They are then published in DCI.
In these output files, there are some general information on the k8s objects used for the test (cronjobs, job and pods) and also an estimation of the downtime.
As an example, for the ROX test case:
```log
>>> Quick gathering object info in the Namespace of test
pod/storage-volume-reader-rox-27742362-ld5l5          0/1     Completed           0          3m20s   10.130.2.151   worker-2   <none>           <none>
pod/storage-volume-reader-rox-27742362-pxlcp          0/1     Completed           0          3m20s   10.130.2.152   worker-2   <none>           <none>
pod/storage-volume-reader-rox-27742364-bfst2          0/1     Completed           0          80s     10.130.2.156   worker-2   <none>           <none>
pod/storage-volume-reader-rox-27742364-xf7ns          0/1     Completed           0          80s     10.130.2.157   worker-2   <none>           <none>
pod/storage-volume-reader-rox-27742365-g5zg7          0/1     Completed           0          20s     10.130.2.159   worker-2   <none>           <none>
pod/storage-volume-reader-rox-27742365-j2kml          0/1     Completed           0          20s     10.130.2.158   worker-2   <none>           <none>
cronjob.batch/storage-volume-reader-rox          */1 * * * *   False     0        20s             123m   volume-reader-rox   registry.dfwt5g.lab:4443/rhel8/support-tools   <none>
job.batch/storage-volume-reader-rox-1664535840          0/1 of 2      101m       101m    volume-reader-rox   registry.dfwt5g.lab:4443/rhel8/support-tools   controller-uid=1ea14747-25a9-4b96-9e30-d38e1cc36709
job.batch/storage-volume-reader-rox-27742362            2/1 of 2      16s        3m20s   volume-reader-rox   registry.dfwt5g.lab:4443/rhel8/support-tools   controller-uid=e4e56035-ce2e-41f0-85a8-4a44958157f9
job.batch/storage-volume-reader-rox-27742364            2/1 of 2      16s        80s     volume-reader-rox   registry.dfwt5g.lab:4443/rhel8/support-tools   controller-uid=1a49e5ab-7660-4487-956f-afcce633b674
job.batch/storage-volume-reader-rox-27742365            2/1 of 2      16s        20s     volume-reader-rox   registry.dfwt5g.lab:4443/rhel8/support-tools   controller-uid=c7872426-3bce-4c81-a8c6-3917185b677d
> Time of the test: 124m
> Number of failures during this time: 1            # Because of the gathering method, this is just an estimation, specially on the last tests could be seens as a failure whereas it was working fine
> Estimated percentage of failure: .800             # 0.8% of down time during the 2h the upgrade was running
```