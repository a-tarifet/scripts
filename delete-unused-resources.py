from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import re

credential = DefaultAzureCredential()
SUBSCRIPTION_ID = "ADD YOUR SUBSCRIPTION HERE"

# Initialize clients
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

def get_resource_group_from_id(resource_id):
    match = re.search(r"/resourceGroups/(?P<rg>[^/]+)/", resource_id, re.IGNORECASE)
    return match.group("rg") if match else None

def find_unattached_nics():
    print("Scanning for unattached NICs...")
    unattached_nics = []
    for nic in network_client.network_interfaces.list_all():
        if not nic.virtual_machine:
            resource_group = get_resource_group_from_id(nic.id)
            if resource_group:
                unattached_nics.append({"name": nic.name, "resource_group": resource_group})
    return unattached_nics

def find_unattached_disks():
    print("Scanning for unattached managed disks...")
    unattached_disks = []
    for disk in compute_client.disks.list():
        if disk.managed_by is None:
            resource_group = get_resource_group_from_id(disk.id)
            if resource_group:
                unattached_disks.append({"name": disk.name, "resource_group": resource_group})
    return unattached_disks

def delete_unused_resources():
    print("Scanning for unused tagged resources...")
    for resource in resource_client.resources.list():
        if resource.tags and resource.tags.get("cleanup") == "true":
            try:
                print(f"Deleting resource: {resource.name} in {resource.resource_group}")
                resource_client.resources.begin_delete_by_id(resource.id, "2021-04-01").result()
            except Exception as e:
                print(f"[ERROR] Failed to delete resource {resource.name}: {str(e)}")

def confirm_and_delete(resource_type, resources, delete_func):
    if not resources:
        print(f"No unused {resource_type}s found.")
        return

    print(f"\nFound the following unused {resource_type}s:")
    for r in resources:
        print(f"- {r['name']} (Resource Group: {r['resource_group']})")

    confirm = input(f"\nDo you want to delete these {resource_type}s? (Y/N): ").strip().lower()
    if confirm == 'y':
        for r in resources:
            try:
                delete_func(r['resource_group'], r['name']).result()
                print(f"Deleted {resource_type}: {r['name']}")
            except Exception as e:
                print(f"[ERROR] Failed to delete {resource_type} {r['name']}: {str(e)}")
    else:
        print(f"Skipping deletion of {resource_type}s.")

if __name__ == "__main__":
    nics = find_unattached_nics()
    confirm_and_delete("NIC", nics, network_client.network_interfaces.begin_delete)

    disks = find_unattached_disks()
    confirm_and_delete("disk", disks, compute_client.disks.begin_delete)

    delete_unused_resources()

    print("\n\u2705 Cleanup completed.")
