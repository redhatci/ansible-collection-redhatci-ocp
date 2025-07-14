# Design Decisions for the `test_report_send` Role

## Abstract

The role generates an event from CI metadata and test reports, and sends this event to the reporting system.

## Table of Contents

1. [Event Structure](event.md)
    1. [metadata generation](metadata.md), per CI:
        1. [DCI](dci.md)
        2. [Jenkins](jenkins.md)
2. [Reporting](reporting.md), per reporting system:
    1. [Splunk](splunk.md)
