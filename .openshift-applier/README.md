

# OpenShift Applier for App

This is an OpenShift applier inventory. See the CI/CD repo for docs.

# Usage

Right now limited to using ansible on your localhost.

1. `[.openshift-applier]$ ansible-galaxy install -r requirements.yml --roles-path=roles --f`

3. `[.openshift-applier]$ ansible-playbook apply.yml -i inventory/ --extra-vars="target=apps"`

See the inventory for the filter tag options.